package com.example.datvemaybay

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentTransaction
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.data.adapter.DateAdapter
import com.example.datvemaybay.data.adapter.FlightAdapter
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.ChuyenBay
import com.example.datvemaybay.data.models.ChuyenBayRequest
import com.example.datvemaybay.data.models.ChuyenBayResponse
import com.example.datvemaybay.ui.homepage.ConfirmFlightFragment
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.text.SimpleDateFormat
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.Locale
import java.util.concurrent.TimeUnit
import kotlin.properties.Delegates

class ChooseFlightActitvity : AppCompatActivity() {

    private lateinit var flightAdapter: FlightAdapter
    private lateinit var recyclerView: RecyclerView
    private lateinit var rvDates: RecyclerView
    private lateinit var tvNoDataText: TextView
    private val confirmFlightList = mutableListOf<ChuyenBay>()


    // Param variables
    private lateinit var sanBayDi: String
    private lateinit var sanBayDen: String
    private lateinit var sanBayDiID: String
    private lateinit var sanBayDenID: String
    private lateinit var ngayDi: String
    private lateinit var ngayVe: String
    private var soLuongKhach by Delegates.notNull<Int>()
    private lateinit var loaiGhe: String
    private var khuHoi by Delegates.notNull<Boolean>()
    private lateinit var tvDetails: TextView
    private lateinit var tvFromFlight: TextView
    private lateinit var tvToFlight: TextView
    private lateinit var btnBack: ImageButton
    private lateinit var selectedFlightContainer: LinearLayout
    private lateinit var tvDepartureTime: TextView
    private lateinit var tvAirlineDetails: TextView
    private lateinit var btnChange: Button

    @SuppressLint("SetTextI18n")
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_choose_flight)

        recyclerView = findViewById(R.id.rvFlightList)
        recyclerView.layoutManager = LinearLayoutManager(this)

        rvDates = findViewById(R.id.dateRecyclerView)
        tvNoDataText = findViewById(R.id.noDataText)
        tvDetails = findViewById(R.id.tvDetails)
        tvFromFlight = findViewById(R.id.tvFromFlight)
        tvToFlight = findViewById(R.id.tvToFlight)
        btnBack = findViewById(R.id.backButton)
        selectedFlightContainer = findViewById(R.id.selectedFlightContainer)
        tvDepartureTime = findViewById(R.id.tvDepartureTime)
        tvAirlineDetails = findViewById(R.id.tv_airline_detail)
        btnChange = findViewById(R.id.btnChange)

        // Lấy tham số tìm kiếm và cập nhật lên giao diện
        getSearchParam()

        // Gán adapter cho từng card trong recycleView để truyền dữ liệu
        flightAdapter = FlightAdapter { selectedFlight ->
            // Xử lý nếu chuyến bay khứ hồi
            if (khuHoi) {
                if (selectedFlightContainer.visibility == View.GONE) {
                    Log.d("ChooseFlightActivity", "Flight được chọn: ${selectedFlight.maChuyenBay}")
                    confirmFlightList.add(selectedFlight)
                    selectedFlightContainer.visibility = View.VISIBLE
                    tvDepartureTime.text = "${convertIsoToDateFormat(selectedFlight.thoiGianDi)}  •  ${extractTime(selectedFlight.thoiGianDi)} - ${extractTime(selectedFlight.thoiGianDen)}"
                    tvAirlineDetails.text = "${selectedFlight.hangHangKhong}  •  ${selectedFlight.loaiGhe}  •  ${selectedFlight.maChuyenBay}"

                    // Tải dữ liệu chuyến bay (khứ hồi) lên theo chiều ngược lại
                    fillDataForReturnFlight()
                }
                else if (selectedFlightContainer.visibility == View.VISIBLE) {
                    // Nếu đã có chuyến đi được chọn
                    Log.d("ChooseFlightActivity", "Flight được chọn: ${selectedFlight.maChuyenBay}")
                    val gapTime = calculateHourDifference(confirmFlightList[0].thoiGianDen, selectedFlight.thoiGianDi)
                    Log.d("ChooseFlightActivity", "Gap thời gian: $gapTime")
                    if (gapTime >= 6) {
                        if (confirmFlightList.size >= 2) {
                            confirmFlightList.removeAt(confirmFlightList.size - 1)
                        }
                        confirmFlightList.add(selectedFlight)
                        val confirmFlightFragment = ConfirmFlightFragment()
                        setDataForConfirmFlightList(confirmFlightFragment)
                        replaceFragment(confirmFlightFragment)
                    }
                    else { // Hiện thông báo
                        Toast.makeText(this@ChooseFlightActitvity, "Vui lòng chọn chuyến bay cách ít nhất 6 giờ sau giờ đến của chuyến bay trước.", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            else // Xử lý nếu chuyến bay không khứ hồi
            {
                Log.d("ChooseFlightActivity", "Flight được chọn: ${selectedFlight.maChuyenBay}")
                confirmFlightList.clear()
                confirmFlightList.add(selectedFlight)
                val confirmFlightFragment = ConfirmFlightFragment()
                setDataForConfirmFlightList(confirmFlightFragment)
                replaceFragment(confirmFlightFragment)
            }
        }

        // Lấy danh sách chuyến bay theo kết quả tìm kiếm
        val request = ChuyenBayRequest(
            san_bay_di = sanBayDiID,
            san_bay_den = sanBayDenID,
            ngay_di = ngayDi,
            so_luong_khach = soLuongKhach,
            loai_ghe = loaiGhe,
            khu_hoi = false,
            ngay_ve = ngayVe,
        )

        Log.d("Sân bay", "Load dữ liệu ban đầu của sân bay lên")
        searchFlights(request)

        // Lấy danh sách ngày xung quanh ngày được chọn
        getDatesForFlight(request)

        // Xử lý sự kiện khi bấm vào btnBack
        btnBack.setOnClickListener {
            finish()
        }

        // Xử lý sự kiện khi bấm vào nút btnChange
        btnChange.setOnClickListener {
            selectedFlightContainer.visibility = View.GONE
            confirmFlightList.removeAt(0)
        }


    }

    // Lấy danh sách chuyến bay
    @SuppressLint("SetTextI18n")
    private fun searchFlights(request: ChuyenBayRequest) {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)

        Log.d("Sân bay", "Sân bay đi: $sanBayDi")
        Log.d("Sân bay", "Sân bay đến: $sanBayDen")
        // Gửi yêu cầu
        apiService.getChuyenBay(request).enqueue(object : Callback<ChuyenBayResponse> {
            @SuppressLint("SetTextI18n")
            override fun onResponse(call: Call<ChuyenBayResponse>, response: Response<ChuyenBayResponse>) {
                if (response.isSuccessful) {
                    val chuyenBayResponse = response.body()
                    if (chuyenBayResponse != null) {
                        if (chuyenBayResponse.directFlight.isNotEmpty()) {
                            flightAdapter.setData(chuyenBayResponse.directFlight)
                            recyclerView.adapter = flightAdapter
                            Log.d("AirportAdapter", "Dữ liệu đã được cập nhật: " + chuyenBayResponse.directFlight.toString())
                        }
                        else {
                            flightAdapter.setData(emptyList())
                            Log.e("API Response", "Không có chuyến bay nào được tìm thấy")
                        }
                        updateData()
                        tvDetails.text = "${request.ngay_di}   •   $soLuongKhach hành khách  •   $loaiGhe"
                    }
                } else {
                    Toast.makeText(this@ChooseFlightActitvity, "Lỗi: ${response.message()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<ChuyenBayResponse>, t: Throwable) {
                Toast.makeText(this@ChooseFlightActitvity, "Lỗi kết nối: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })

    }

    // Hàm chuyển đổi định dạng EEE, dd MMM yyyy sang dạng dd-MM-yyyy
    private fun transformToFormattedDate(date: String): String {
        return try {
            val inputFormatter = android.icu.text.SimpleDateFormat("EEE, dd MMM yyyy", Locale.ENGLISH)
            val outputFormatter = android.icu.text.SimpleDateFormat("dd-MM-yyyy", Locale.ENGLISH)
            val parsedDate = inputFormatter.parse(date) ?: throw IllegalArgumentException("Invalid date format: $date")
            outputFormatter.format(parsedDate)
        } catch (e: Exception) {
            ""
        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun generateDateList(selectedDate: LocalDate, returnDate: LocalDate? = null): List<String> {
        return if (returnDate != null) {
            val dateList = mutableListOf<String>()
            var currentDate = selectedDate
            while (!currentDate.isAfter(returnDate)) {
                dateList.add(formatDate(currentDate))
                currentDate = currentDate.plusDays(1)
            }
            dateList
        } else {
            val startDate = selectedDate.minusDays(5)
            val endDate = selectedDate.plusDays(5)
            (startDate..endDate).map { formatDate(it) }
        }
    }

    // Extension để hỗ trợ range cho LocalDate
    @RequiresApi(Build.VERSION_CODES.O)
    operator fun LocalDate.rangeTo(other: LocalDate): List<LocalDate> {
        val dates = mutableListOf<LocalDate>()
        var current = this
        while (!current.isAfter(other)) {
            dates.add(current)
            current = current.plusDays(1)
        }
        return dates
    }

    // format về dạng EEE, dd MMM yyyy
    @RequiresApi(Build.VERSION_CODES.O)
    fun formatDate(date: LocalDate): String {
        val formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy", Locale.ENGLISH)
        return date.format(formatter)
    }

    // Hàm lấy dữ liệu chuyến bay của các ngày trong xung quanh ngày tìm kiếm
    @RequiresApi(Build.VERSION_CODES.O)
    private fun getDatesForFlight(request: ChuyenBayRequest) {
        val ngayDiDate: LocalDate = parseDate(ngayDi)
        val ngayVeDate: LocalDate = if (ngayVe == "N/A" || ngayVe.isEmpty()) {
            ngayDiDate.plusDays(5)
        } else parseDate((ngayVe))

        Log.d("AirportAdapter", "Dữ liệu đã được cập nhật: $ngayVeDate")

        val dates = generateDateList(ngayDiDate, ngayVeDate)
        val adapter = DateAdapter(dates) { selectedDate ->
            request.ngay_di = transformToFormattedDate(selectedDate)
            searchFlights(request)
        }

        rvDates.layoutManager = LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false)
        rvDates.adapter = adapter
    }

    // Hàm lấy dữ liệu từ MainActitvity truyền đến
    @SuppressLint("SetTextI18n")
    private fun getSearchParam() {
        sanBayDi = intent.getStringExtra("san_bay_di") ?: "N/A"
        sanBayDen = intent.getStringExtra("san_bay_den") ?: "N/A"
        sanBayDiID = intent.getStringExtra("san_bay_di_id") ?: "N/A"
        sanBayDenID = intent.getStringExtra("san_bay_den_id") ?: "N/A"
        ngayDi = transformToFormattedDate(intent.getStringExtra("ngay_di") ?: "N/A")
        soLuongKhach = intent.getIntExtra("so_luong_khach", 0)

        loaiGhe = (intent.getStringExtra("loai_ghe") ?: "N/A").let { it.take(3).uppercase() }
        khuHoi = intent.getBooleanExtra("khu_hoi", false)
        ngayVe = transformToFormattedDate(intent.getStringExtra("ngay_ve") ?: "N/A")

        tvFromFlight.text = sanBayDi
        tvToFlight.text = sanBayDen
        tvDetails.text = "$ngayDi   •   $soLuongKhach hành khách  •   $loaiGhe"
        Log.d("Soluongkhach", "Soluongkhach $soLuongKhach" )
    }

    // Hàm chuyển chuỗi dạng dd-MM-yyyy sang kiểu Date
    @RequiresApi(Build.VERSION_CODES.O)
    fun parseDate(dateString: String, pattern: String = "dd-MM-yyyy"): LocalDate {
        val formatter = DateTimeFormatter.ofPattern(pattern)
        return LocalDate.parse(dateString, formatter)
    }

    // Hàm cập nhật dữ liệu chuyến bay
    private fun updateData() {
        if (flightAdapter.isDataEmpty()) {
            recyclerView.visibility = View.GONE
            tvNoDataText.visibility = View.VISIBLE
        } else {
            recyclerView.visibility = View.VISIBLE
            tvNoDataText.visibility = View.GONE
        }
    }

    @Deprecated("This method has been deprecated in favor of using the\n      {@link OnBackPressedDispatcher} via {@link #getOnBackPressedDispatcher()}.\n      The OnBackPressedDispatcher controls how back button events are dispatched\n      to one or more {@link OnBackPressedCallback} objects.")
    override fun onBackPressed() {
        super.onBackPressed()
        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)
        finish()
    }

    // Hàm gửi dữ liệu cho ConfirmFlightFragment
    private fun setDataForConfirmFlightList(confirmFlightFragment: ConfirmFlightFragment) {
        val bundle = Bundle()
        bundle.putSerializable("FLIGHT_LIST", ArrayList(confirmFlightList))
        confirmFlightFragment.arguments = bundle
    }

    // Hảm lấy HH:mm trong yyyy-MM-dd'T'HH:mm:ss
    fun extractTime(dateTime: String): String {
        val inputFormat =
            android.icu.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        val outputFormat = android.icu.text.SimpleDateFormat("HH:mm", Locale.getDefault())

        return try {
            val date = inputFormat.parse(dateTime)
            outputFormat.format(date)
        } catch (e: Exception) {
            "N/A"
        }
    }

    // Thay thế fragment
    private fun replaceFragment(fragment: Fragment) {
        val transaction: FragmentTransaction = supportFragmentManager.beginTransaction()
        transaction.replace(android.R.id.content, fragment)
        transaction.addToBackStack(null)
        transaction.commit()
    }

    // Hàm tính toán thời gian chênh lệch giữa 2 thời điểm
    private fun calculateHourDifference(startDate: String, endDate: String): Long {
        val dateFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.ENGLISH)

        return try {
            val start = dateFormat.parse(startDate)
            val end = dateFormat.parse(endDate)

            if (start != null && end != null) {
                val diffInMillis = end.time - start.time
                TimeUnit.MILLISECONDS.toHours(diffInMillis)
            } else {
                0
            }
        } catch (e: Exception) {
            e.printStackTrace()
            0
        }
    }

    // Hàm lấy dữ liệu tất cả chuyến bay cho chuyến khứ hồi (return)
    @SuppressLint("NewApi", "SetTextI18n")
    private fun fillDataForReturnFlight() {
        val requestReturn = ChuyenBayRequest(
            san_bay_di = sanBayDenID,
            san_bay_den = sanBayDiID,
            ngay_di = ngayDi,
            so_luong_khach = soLuongKhach,
            loai_ghe = loaiGhe,
            khu_hoi = false,
            ngay_ve = ngayVe,
        )
        // Cập nhật lại dữ liệu chuyến bay
        tvFromFlight.text = sanBayDi
        tvToFlight.text = sanBayDen
        tvDetails.text = "${ngayDi}   •   ${soLuongKhach} hành khách  •   ${loaiGhe}"
        searchFlights(requestReturn)
        getDatesForFlight(requestReturn)
    }

    // Hàm chuyển dữ liệu dạng chuỗi DateTime sang chuỗi dạng dd-MM-yyyy
    @SuppressLint("NewApi")
    fun convertIsoToDateFormat(input: String): String {
        val inputFormatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME
        val outputFormatter = DateTimeFormatter.ofPattern("dd-MM-yyyy")
        val dateTime = LocalDateTime.parse(input, inputFormatter)
        return dateTime.format(outputFormatter)
    }

}