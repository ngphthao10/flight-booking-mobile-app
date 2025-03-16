package com.example.datvemaybay

import android.annotation.SuppressLint
import android.content.Intent
import android.icu.text.SimpleDateFormat
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentTransaction
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.Switch
import androidx.annotation.RequiresApi
import com.example.datvemaybay.data.adapter.AirportAdapter
import com.example.datvemaybay.data.adapter.FlightAdapter
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.ChuyenBayRequest
import com.example.datvemaybay.data.models.ChuyenBayResponse
import com.example.datvemaybay.data.models.SanBay
import com.example.datvemaybay.data.models.SanBayResponse
import com.example.datvemaybay.databinding.ActivityMainBinding
import com.example.datvemaybay.ui.homepage.TravellersFragment
import com.example.datvemaybay.ui.homepage.AirportFragment
import com.example.datvemaybay.ui.homepage.ClassFragment
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.google.android.material.datepicker.CalendarConstraints
import com.google.android.material.datepicker.DateValidatorPointForward
import com.google.android.material.datepicker.MaterialDatePicker
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.Date
import java.util.Locale


@SuppressLint("UseSwitchCompatOrMaterialCode")
class MainActivity: AppCompatActivity(), AirportFragment.OnItemSelectedListener {
    private lateinit var binding: ActivityMainBinding
    private lateinit var airportAdapter: AirportAdapter

    private lateinit var menuIcon: ImageButton
    private lateinit var profileImage: ImageButton
    private lateinit var fromCity: TextView
    private lateinit var toCity: TextView
    private lateinit var fromCityID: TextView
    private lateinit var toCityID: TextView
    private lateinit var swapIcon: ImageButton
    private lateinit var searchFlightsButton: Button
    private lateinit var bottomNav: BottomNavigationView
    private lateinit var fromInput: LinearLayout
    private lateinit var toInput: LinearLayout
    private lateinit var returnDateContainer: LinearLayout
    private lateinit var returnDate: TextView
    private lateinit var departureDate: TextView
    private lateinit var roundTrip: Switch
    private lateinit var departureDateContainer: LinearLayout
    private lateinit var travellersContainer: LinearLayout
    private lateinit var travellers: TextView
    private lateinit var classContainer: LinearLayout
    private lateinit var classType: TextView
    private var totalTravellers : Int = 0



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        // Initialize views
        menuIcon = findViewById(R.id.menuIcon)
        profileImage = findViewById(R.id.profileImage)
        fromCity = findViewById(R.id.fromCity)
        toCity = findViewById(R.id.toCity)
        fromCityID = findViewById(R.id.fromCityCode)
        toCityID = findViewById(R.id.toCityCode)
        swapIcon = findViewById(R.id.swapIcon)
        searchFlightsButton = findViewById(R.id.searchFlightsButton)
        bottomNav = findViewById(R.id.bottom_nav)
        fromInput = findViewById(R.id.fromInput)
        toInput = findViewById(R.id.toInput)
        departureDateContainer = findViewById(R.id.departureDateContainer)
        returnDateContainer = findViewById(R.id.returnDateContainer)
        returnDate = findViewById(R.id.returnDate)
        roundTrip = findViewById(R.id.roundTrip)
        departureDateContainer = findViewById(R.id.departureDateContainer)
        departureDate = findViewById(R.id.departureDate)
        travellersContainer = findViewById(R.id.travellersContainer)
        travellers = findViewById(R.id.travellers)
        classContainer = findViewById(R.id.classContainer)
        classType = findViewById(R.id.classType)


        // Đăng ký sự kiện cho from/to input
        airportInputClick(fromInput, "from")
        airportInputClick(toInput, "to")

        // Đăng ký sự kiện cho switch round trip và departure/return trip
        departureDateContainer.setOnClickListener {
            showNormalCalendar()
        }
        getRoundTrip()

        // Đăng ký sự kiện cho traveller/ class input
        travellersInputClick()
        classInputClick()

        // Đăng ký sự kiện khi nhấn vào nút Search Flight
        searchFlightsButton.setOnClickListener {
            val sanBayDiID = fromCityID.text.toString().trim()
            val sanBayDenID = toCityID.text.toString().trim()
            val sanBayDi = fromCity.text.toString().trim()
            val sanBayDen = toCity.text.toString().trim()
            val ngayDi = departureDate.text.toString().trim()
            val soLuongKhach = travellers.text.toString().trim()
            val loaiGhe = classType.text.toString().trim()
            val ngayVe = returnDate.text.toString().trim()
            val khuHoi = roundTrip.isChecked

            if (sanBayDi.isEmpty() || sanBayDen.isEmpty() || ngayDi.isEmpty() || soLuongKhach.isEmpty() || loaiGhe.isEmpty()) {
                Toast.makeText(this, "Vui lòng điền đầy đủ thông tin!", Toast.LENGTH_SHORT).show()
            } else {
                val intent = Intent(this@MainActivity, ChooseFlightActitvity::class.java)
                intent.putExtra("san_bay_di_id", sanBayDiID)
                intent.putExtra("san_bay_den_id", sanBayDenID)
                intent.putExtra("san_bay_di", sanBayDi)
                intent.putExtra("san_bay_den", sanBayDen)
                intent.putExtra("ngay_di", ngayDi)
                intent.putExtra("so_luong_khach", totalTravellers)
                intent.putExtra("loai_ghe", loaiGhe)
                intent.putExtra("khu_hoi", khuHoi)
                Log.d("ChooseFlightActivity", "Flight được chọn: $khuHoi")
                intent.putExtra("ngay_ve", ngayVe)
                startActivity(intent)
            }
        }


    }

    private fun replaceFragment(fragment: Fragment) {
        val transaction: FragmentTransaction = supportFragmentManager.beginTransaction()
        transaction.replace(android.R.id.content, fragment)
        transaction.addToBackStack(null)
        transaction.commit()
    }

    private fun getSanBayList() {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val call: Call<SanBayResponse> = apiService.getSanBayList()

        call.enqueue(object : Callback<SanBayResponse> {
            override fun onResponse(call: Call<SanBayResponse>, response: Response<SanBayResponse>) {
                if (response.isSuccessful) {
                    val sanBayResponse = response.body()
                    if (sanBayResponse != null) {
                        // Cập nhật dữ liệu lên RecyclerView
                        airportAdapter.setData(sanBayResponse.data)
                        Log.d("AirportAdapter", "Dữ liệu đã được cập nhật: " + sanBayResponse.data.toString());
                    }
                } else {
                    Toast.makeText(this@MainActivity, "Lỗi: ${response.message()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<SanBayResponse>, t: Throwable) {
                Toast.makeText(this@MainActivity, "Lỗi kết nối: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }

    override fun onItemSelected(item: SanBay, input: String) {
        if (input == "from") {
            fromCity.text = item.thanhPho
            fromCityID.text = item.maSanBay
        } else if (input == "to") {
            toCity.text = item.thanhPho
            toCityID.text = item.maSanBay
        }
        supportFragmentManager.popBackStack()
    }

    private fun airportInputClick(input: LinearLayout, inputType: String) {
        input.setOnClickListener {
            airportAdapter = AirportAdapter { item ->
                onItemSelected(item, inputType)
            }
            val airportFragment = AirportFragment.newInstance(airportAdapter, inputType)
            replaceFragment(airportFragment)

            // Đợi Fragment được gắn vào Activity
            supportFragmentManager.executePendingTransactions()

            // Lấy RecyclerView từ Fragment
            val recyclerView = airportFragment.recyclerView
            recyclerView.adapter = airportAdapter
            getSanBayList()
        }
    }

    // Hiển thị DateRangePicker khi bấm vào nút "Add Return Date"
    private fun showDateRangePicker() {
        // Tạo bộ chọn ngày dạng range
        val builder = MaterialDatePicker.Builder.dateRangePicker()

        // Thiết lập các hạn chế lịch (nếu có)
        val constraintsBuilder = CalendarConstraints.Builder()
            .setValidator(DateValidatorPointForward.now()) // Chỉ cho phép chọn ngày từ hiện tại trở đi
        builder.setCalendarConstraints(constraintsBuilder.build())

        val dateRangePicker = builder.build()

        // Xử lý khi người dùng chọn ngày
        dateRangePicker.addOnPositiveButtonClickListener { selection ->
            val startDate = selection.first
            val endDate = selection.second

            // Chuyển đổi ngày từ Long thành Date để hiển thị
            val sdf = SimpleDateFormat("EEE, dd MMM yyyy", Locale.getDefault())
            val startDateString = sdf.format(Date(startDate))
            val endDateString = sdf.format(Date(endDate))

            // Hiển thị ngày đi và ngày về
            departureDate.text = startDateString
            returnDate.text = endDateString
        }

        // Hiển thị picker vào supportFragmentManager
        dateRangePicker.show(supportFragmentManager, dateRangePicker.toString())
    }

    // Hiển thị Calendar bình thường
    @SuppressLint("PrivateResource")
    private fun showNormalCalendar() {
        val builder = MaterialDatePicker.Builder.datePicker()

        // Thiết lập các hạn chế lịch (nếu có)
        val constraintsBuilder = CalendarConstraints.Builder()
            .setValidator(DateValidatorPointForward.now())
        builder.setCalendarConstraints(constraintsBuilder.build())

        val materialDatePicker = builder.build()

        // Xử lý khi người dùng chọn ngày
        materialDatePicker.addOnPositiveButtonClickListener { selection ->
            val sdf = SimpleDateFormat("EEE, dd MMM yyyy", Locale.getDefault())
            val selectedDate = sdf.format(Date(selection))

            // Hiển thị ngày đi
            departureDate.text = selectedDate
        }

        // Hiển thị picker vào supportFragmentManager
        materialDatePicker.show(supportFragmentManager, materialDatePicker.toString())
    }

    // Sự kiện nhấn nút switch
    private fun getRoundTrip() {
        roundTrip.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                returnDateContainer.visibility = View.VISIBLE
                departureDateContainer.setOnClickListener {
                    showDateRangePicker()
                }
                returnDateContainer.setOnClickListener {
                    showDateRangePicker()
                }
            } else {
                returnDateContainer.visibility = View.GONE
                departureDateContainer.setOnClickListener {
                    showNormalCalendar()
                }
                returnDate.text = ""
            }
        }
    }

    // Xử lý sự kiện khi nhấn vào ô travellers
    @SuppressLint("SetTextI18n")
    private fun travellersInputClick() {

        val sharedPreferences = getSharedPreferences("AppPreferences", MODE_PRIVATE)
        var adultCount = sharedPreferences.getInt("adult_count", 0)
        var childCount = sharedPreferences.getInt("child_count", 0)
        var infantCount = sharedPreferences.getInt("infant_count", 0)

        totalTravellers = adultCount + childCount + infantCount
        travellers.text = "$totalTravellers hành khách"

        // Xử lý khi nhấn vào travellers input
        travellersContainer.setOnClickListener {
            val travellersFragment = TravellersFragment.newInstance(adultCount, childCount, infantCount)
            travellersFragment.show(supportFragmentManager, travellersFragment.tag)
        }

        // Nhận dữ liệu trả về từ TravellersFragment
        supportFragmentManager.setFragmentResultListener("travellers_result", this) { _, bundle ->
            adultCount = bundle.getString("adult_count", "0").toInt()
            childCount = bundle.getString("child_count", "0").toInt()
            infantCount = bundle.getString("infant_count", "0").toInt()

            // Lưu dữ liệu vào SharedPreferences
            sharedPreferences.edit().apply {
                putInt("adult_count", adultCount)
                putInt("child_count", childCount)
                putInt("infant_count", infantCount)
                apply()
            }

            // Cập nhật TextView hiển thị
            val updatedTotalTravellers = adultCount + childCount + infantCount
            travellers.text = "$updatedTotalTravellers hành khách"
        }
    }


    // Xử lý sự kiện khi nhấn vào class input
    private fun classInputClick() {
        supportFragmentManager.setFragmentResultListener("class_result", this) { _, bundle ->
            val classSeat = bundle.getString("class_result", "Economy")

            val sharedPreferences = getSharedPreferences("AppPreferences", MODE_PRIVATE)
            sharedPreferences.edit().putString("class_result", classSeat).apply()

            classType.text = classSeat
        }

        classContainer.setOnClickListener {
            // Hiển thị BottomSheet
            val sharedPreferences = getSharedPreferences("AppPreferences", MODE_PRIVATE)
            val classSeat = sharedPreferences.getString("class_result", null)

            val bottomSheet = ClassFragment.newInstance(classSeat)
            bottomSheet.show(supportFragmentManager, "classType")
        }
    }




}