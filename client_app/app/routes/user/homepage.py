from flask import Blueprint, render_template, flash, url_for, redirect, request, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import requests
from datetime import datetime, timedelta
from flask import current_app 

homepage = Blueprint('homepage', __name__)
@homepage.route('/', methods=['GET'])
def home():
    try:
        user_info = session.get('user_info')

        response = requests.get(f"{current_app.config['API_URL']}/api/sanbay")
        response.raise_for_status()
        sanbay_list = response.json()

        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        default_data = {
            'departure_date': today.strftime('%d-%m-%Y'),
            'return_date': tomorrow.strftime('%d-%m-%Y'),
            'passenger_adults': 1,
            'passenger_children': 0,
            'passenger_infants': 0,
            'seat_class': [
                {'value': 'ECO', 'label': 'Hạng phổ thông'},
                {'value': 'BUS', 'label': 'Hạng thương gia'}
            ],
            'is_round_trip': True
        }

        return render_template(
            'user/homepage.html',
            san_bay=sanbay_list,
            default_data=default_data,
            api_url=current_app.config['API_URL'],
            user_info=user_info
        )

    except Exception as e:
        error_message = f"Lỗi hệ thống: {str(e)}"
        flash(error_message, 'danger')
        return render_template(
            'user/homepage.html',
            san_bay=[],
            default_data={},
            error=error_message,
            api_url=current_app.config['API_URL'],
            user_info=None
        )

@homepage.route('/search-flights', methods=['GET', 'POST'])
def search_flights():
    try:
        processed_results = {
            'direct_flights': [],
            'connecting_flights': [],
            'return_direct_flights': [],
            'return_connecting_flights': []
        }
        search_params = {}

        if request.method == 'POST':
            origin = request.form.get('origin')
            destination = request.form.get('destination')
            departure_date = datetime.strptime(request.form.get('departure-date'), '%Y-%m-%d').strftime('%d-%m-%Y') 
            return_date = request.form.get('return-date')
            seat_class = request.form.get('seat_class', 'ECO')
            adults = int(request.form.get('nguoiLon', 1))
            children = int(request.form.get('treEm', 0))
            infants = int(request.form.get('emBe', 0))
            is_round_trip = request.form.get('return-trip') == 'on'

            if not all([origin, destination, departure_date]):
                flash('Vui lòng điền đầy đủ thông tin tìm kiếm', 'warning')
                return redirect(url_for('homepage.home'))
                
            search_data = {
                'san_bay_di': origin,
                'san_bay_den': destination,
                'ngay_di': departure_date,
                'so_luong_khach': adults + children,
                'loai_ghe': seat_class,
                'khu_hoi': is_round_trip,
                'include_connecting': True,
                'max_stops': 2
            }

            if is_round_trip and return_date:
                search_data['ngay_ve'] = datetime.strptime(return_date, '%Y-%m-%d').strftime('%d-%m-%Y')
            else:
                search_data['ngay_ve'] = ''

            response = requests.post(
                f"{current_app.config['API_URL']}/api/flights/search",
                json=search_data
            )
            response.raise_for_status()
            flight_results = response.json()

            if flight_results.get('direct_flights'):
                processed_results['direct_flights'].extend(flight_results['direct_flights'])
            if flight_results.get('connecting_flights'):
                processed_results['connecting_flights'].extend(flight_results['connecting_flights'])
            if flight_results.get('return_direct_flights'):
                processed_results['return_direct_flights'].extend(flight_results['return_direct_flights'])
            if flight_results.get('return_connecting_flights'):
                processed_results['return_connecting_flights'].extend(flight_results['return_connecting_flights'])

            search_params = {
                'origin': origin,
                'destination': destination,
                'departure_date': departure_date,
                'return_date': datetime.strptime(return_date, '%Y-%m-%d').strftime('%d-%m-%Y') ,
                'adults': adults,
                'children': children,
                'infants': infants,
                'seat_class': seat_class,
                'is_round_trip': is_round_trip
            }
            print(search_params)
            session['search_params'] = search_params
            session['flight_results'] = processed_results

        else:
            search_params = session.get('search_params', {})
            processed_results = session.get('flight_results', processed_results)

        try:
            sanbay_response = requests.get(f"{current_app.config['API_URL']}/api/sanbay")
            sanbay_response.raise_for_status()
            sanbay_list = sanbay_response.json()
        except:
            sanbay_list = []

        all_flights = []
        for flight_type in ['direct_flights', 'return_direct_flights']:
            if processed_results.get(flight_type):
                all_flights.extend(processed_results[flight_type])
        for connection_type in ['connecting_flights', 'return_connecting_flights']:
            if processed_results.get(connection_type):
                for connection in processed_results[connection_type]:
                    all_flights.extend(connection['flights'])

        price_range = {'min': float('inf'), 'max': 0}
        airlines_stats = {
            'QH': {'name': 'Bamboo Airways', 'count': 0},
            'VJ': {'name': 'VietJet Air', 'count': 0},
            'VN': {'name': 'Vietnam Airlines', 'count': 0}, 
            'VU': {'name': 'Vietravel Airlines', 'count': 0}
        }

        for flight in all_flights:
            airline = flight['ma_hhk']
            if airline in airlines_stats:
                airlines_stats[airline]['count'] += 1

            for price_type in ['gia_ve_eco', 'gia_ve_bus']:
                if flight.get(price_type):
                    price_range['min'] = min(price_range['min'], flight[price_type])
                    price_range['max'] = max(price_range['max'], flight[price_type])

        if price_range['min'] == float('inf'):
            price_range['min'] = 0

        if request.args.get('filtered'):
            filter_params = {
                'flight_type': request.args.get('flight_type', 'all'),
                'airlines': request.args.getlist('airlines[]'),
                'departure_time': request.args.getlist('departure_time[]'),
                'arrival_time': request.args.getlist('arrival_time[]'),
                'max_price': float(request.args.get('max_price', float('inf')))
            }
            
            try:
                filter_response = requests.post(
                    f"{current_app.config['API_URL']}/api/flights/filter",
                    json={
                        'flights': processed_results,
                        'filters': filter_params
                    }
                )
                filter_response.raise_for_status()
                filter_results = filter_response.json()
                
                if filter_results['status'] == 'success':
                    processed_results = filter_results['data']
            except Exception as e:
                print(f"Filter Error: {str(e)}")
                flash('Lỗi khi lọc kết quả', 'danger')
        
        return render_template(
            'user/flight_results.html',
            san_bay=sanbay_list,
            search_params=search_params,
            flight_results=processed_results,
            price_range=price_range,
            airlines_stats=airlines_stats,
            api_url=current_app.config['API_URL']
        )
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        flash(f'Lỗi kết nối đến server: {str(e)}', 'danger')
        return redirect(url_for('homepage.home'))
    except Exception as e:
        print(f"General Error: {str(e)}")
        flash(f'Đã xảy ra lỗi: {str(e)}', 'danger')
        return redirect(url_for('homepage.home'))


# Định nghĩa filters cho blueprint
@homepage.app_template_filter('format_price')
def format_price(value):
    if not value:
        return "0 VND"
    return f"{int(value):,} VND"

@homepage.app_template_filter('time')
def format_time(datetime_str):
    if not datetime_str:
        return ""
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')

@homepage.app_template_filter('duration')
def format_duration(hours):
    if not hours:
        return "0h 0m"
    return f"{int(hours)}h {int((hours % 1) * 60)}m"

@homepage.app_template_filter('datetime')
def parse_datetime(date_str):
    if not date_str:
        return datetime.now()
    return datetime.strptime(date_str, '%d-%m-%Y')

@homepage.app_template_filter('days_offset')
def days_offset(date, offset):
    if not date:
        return datetime.now()
    return date + timedelta(days=offset)

@homepage.app_template_filter('weekday_short')
def weekday_short(date):
    if not date:
        return ""
    weekdays = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
    return weekdays[date.weekday()]

@homepage.app_template_filter('min_price')
def min_price(flights):
    if not flights:
        return 0
    try:
        return min(flight.get('gia_ve_eco', float('inf')) for flight in flights if flight)
    except:
        return 0

@homepage.app_template_filter('min_duration_price')
def min_duration_price(flights):
    if not flights:
        return 0
    try:
        valid_flights = [flight for flight in flights if flight and flight.get('thoi_gian_bay', float('inf')) <= 3]
        if valid_flights:
            return min(flight.get('gia_ve_eco', float('inf')) for flight in valid_flights)
        return 0
    except:
        return 0

@homepage.app_template_filter('direct_flight_price')
def direct_flight_price(flights):
    if not flights:
        return 0
    try:
        direct_flights = [f for f in flights if f and f.get('san_bay_di') and f.get('san_bay_den') 
                         and f['san_bay_di'] != f['san_bay_den']]
        if direct_flights:
            return min(f.get('gia_ve_eco', float('inf')) for f in direct_flights)
        return 0
    except:
        return 0