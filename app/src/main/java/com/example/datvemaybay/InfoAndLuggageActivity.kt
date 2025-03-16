package com.example.datvemaybay

import BookingResponse
import DVHL
import Flight
import FlightBooking
import HanhKhach
import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentTransaction
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.data.adapter.InfoAndLuggageAdapter
import com.example.datvemaybay.data.adapter.PassengerAdapter
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.ContactPerson
import com.example.datvemaybay.data.models.DatChoData
import com.example.datvemaybay.data.models.HanhLyPassenger
import com.example.datvemaybay.data.models.PassengerInfo
import com.example.datvemaybay.data.viewmodel.ContactPersonViewModel
import com.example.datvemaybay.data.viewmodel.LuggageViewModel
import com.example.datvemaybay.data.viewmodel.PassengerViewModel
import com.example.datvemaybay.ui.homepage.ContactPersonFragment
import com.example.datvemaybay.ui.homepage.LuggageFragment
import com.example.datvemaybay.ui.homepage.PassengerInfoFragment
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.text.DecimalFormat

class InfoAndLuggageActivity : AppCompatActivity() {

    // Init params
    private lateinit var btnAddContactPerson: ImageButton
    private lateinit var tvContactPerson: TextView
    private lateinit var btnSelectHanhLy: Button
    private lateinit var noteLuggage: TextView
    private lateinit var labelTongTien: TextView
    private lateinit var tvTongTien: TextView
    private lateinit var btnContinue: Button
    private lateinit var btnBack: ImageButton

    private lateinit var bookingList: ArrayList<DatChoData> // Lưu chuyến bay với giá gói
    private lateinit var luggageList: MutableMap<Int, MutableList<HanhLyPassenger>>// Lưu hành lý
    private lateinit var contactPersonInfo: ContactPerson // Lưu người liên hệ
    private var passengerInfoList: ArrayList<PassengerInfo> = ArrayList()// Lưu thông tin hành khách

    private lateinit var adapter: InfoAndLuggageAdapter
    private var tongTien: Long = 0
    private var tongHanhLy: Long = 0
    private var isPassengerValid: Boolean = false

    private val passengerViewModel: PassengerViewModel by viewModels()
    private val passengerTitles = mutableListOf<String>()
    private lateinit var contactViewModel: ContactPersonViewModel
    private lateinit var luggageViewModel: LuggageViewModel

    // Biến lưu tổng data
    private var flightBooking: FlightBooking = FlightBooking()
    private lateinit var bookingResponseData: BookingResponse

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_info_and_luggage)

        // Khai báo các phần tử view
        btnAddContactPerson = findViewById(R.id.btnAddNguoiLienHe)
        tvContactPerson = findViewById(R.id.tvContactPerson)
        btnSelectHanhLy = findViewById(R.id.selectHanhLy)
        noteLuggage = findViewById(R.id.selectLuggage)
        labelTongTien = findViewById(R.id.labelTongTien)
        tvTongTien = findViewById(R.id.tvTongTien)
        btnContinue = findViewById(R.id.btnContinue)
        btnBack = findViewById(R.id.backButton)


        // Nhận bookingList từ Intent
        bookingList = intent.getSerializableExtra("BOOKING_DATA") as? ArrayList<DatChoData>
            ?: ArrayList()

        Log.d("BookingList", "Danh sách đặt chỗ $bookingList")

        // Lấy dữ liệu chuyến bay cho FlightBooking
        flightBooking.chuyenBay = populateFlightBooking(bookingList)


        // Thiết lập RecyclerView và Adapter cho thông tin vé
        val recyclerView = findViewById<RecyclerView>(R.id.bookingData)
        recyclerView.layoutManager = LinearLayoutManager(this)
        adapter = InfoAndLuggageAdapter(bookingList)
        recyclerView.adapter = adapter

        // Thiết lập RecycleView và Adapter cho thông tin hành khách
        getPassenger()

        // Lấy dữ liệu hành khách
        getPassengerInfoFromFragment()
        calculateTotalPrice()
        getContactPersonData()
        getLuggageData()


        // Lấy dữ liệu người liên hệ


        // Xử lý sự kiện khi bấm vào nút addNguoiLienHe
        val contactPersonFragment = ContactPersonFragment()
        btnAddContactPerson.setOnClickListener {
            replaceFragment(contactPersonFragment)
        }

        // Xử lý sự kiện khi bấm nút chọn Hành lý
        val luggageFragment = LuggageFragment.newInstance(bookingList, java.util.ArrayList(passengerTitles))
        btnSelectHanhLy.setOnClickListener {
            Log.d("HAHA", "Dữ liệu passengerTitles $passengerTitles")
            replaceFragment(luggageFragment)
        }

        btnBack.setOnClickListener {
            supportFragmentManager.popBackStack()
        }

        Log.d("HAHA", "Dữ liệu gửi đi $flightBooking")

//        btnContinue.isEnabled = false
    }


    // Thay thế fragment
    private fun replaceFragment(fragment: Fragment) {
        val transaction: FragmentTransaction = supportFragmentManager.beginTransaction()
        transaction.replace(android.R.id.content, fragment)
        transaction.addToBackStack(null)
        transaction.commit()
    }

    // Hàm lấy phân loại hàng khách
    private fun getPassenger() {
        // Lấy dữ liệu từ SharedPreferences
        val sharedPreferences = getSharedPreferences("AppPreferences", MODE_PRIVATE)
        val adultCount = sharedPreferences.getInt("adult_count", 0)
        val childCount = sharedPreferences.getInt("child_count", 0)
        val infantCount = sharedPreferences.getInt("infant_count", 0)

        passengerTitles.clear()
        // Thêm người lớn
        for (i in 1..adultCount) {
            passengerTitles.add("Người lớn $i")
        }
        // Thêm trẻ em
        for (i in 1..childCount) {
            passengerTitles.add("Trẻ em $i")
        }
        // Thêm trẻ sơ sinh
        for (i in 1..infantCount) {
            passengerTitles.add("Trẻ sơ sinh $i")
        }

        // Gán adapter cho RecyclerView
        val passengerAdapter = PassengerAdapter(passengerTitles) { passengerTitle ->
            // Xử lý khi item được bấm
            val fragment = PassengerInfoFragment.newInstance(passengerTitle)
            replaceFragment(fragment)
        }
        val rvPassengerList = findViewById<RecyclerView>(R.id.rvPassengerList)
        rvPassengerList.layoutManager = LinearLayoutManager(this)
        rvPassengerList.adapter = passengerAdapter
    }

    @SuppressLint("SetTextI18n")
    private fun getPassengerInfoFromFragment() {
        // Quan sát LiveData của ViewModel để nhận thông tin hành khách
        passengerViewModel.passengerData.observe(this) { passengerMap ->
            passengerMap?.forEach { (id, passenger) ->
                val passengerIndex = passengerTitles.indexOf(id)
                passengerInfoList.add(passenger)
//                Log.d("Nguoi lien he", "Nguoi lien he $id $passenger")

                if (passengerIndex != -1) {
                    // Cập nhật RecyclerView nếu tìm thấy hành khách tương ứng
                    val rvPassengerList = findViewById<RecyclerView>(R.id.rvPassengerList)
                    val viewHolder = rvPassengerList.findViewHolderForAdapterPosition(passengerIndex) as? PassengerAdapter.PassengerViewHolder

                    viewHolder?.let {
                        // Gán họ và tên cho TextView rvHoTen
                        it.itemView.findViewById<TextView>(R.id.edtHoTen)?.text = "${passenger.title} ${passenger.lastName} ${passenger.firstName}"
                    }
                }
            }
            Log.d("Hành kahchs", "danh sách hành khachcs $passengerInfoList")
            if (passengerInfoList.isNotEmpty()) {
                flightBooking.hanhKhach = populateHanhKhach(passengerInfoList)
            }
        }

    }

    // Hàm lấy dữ liệu của ContactPerson
    @SuppressLint("SetTextI18n")
    private fun getContactPersonData (){
        contactViewModel = ViewModelProvider(this)[ContactPersonViewModel::class.java]

        // Observe changes to the contact person data
        contactViewModel.contactPersonData.observe(this) { contactPerson ->
            contactPerson?.let {
                Log.d("Contact", "Contact person $contactPerson")
                tvContactPerson.text = "${contactPerson.ho} ${contactPerson.ten}\n${contactPerson.email}  -  +84${contactPerson.phoneNumber}"
                contactPersonInfo = contactPerson
            }
            Log.d("Nguoi lien he", "Nguoi lien he $contactPersonInfo")
//            val emptyContactPerson = ContactPerson()
            if (contactPerson != null) {
                flightBooking.nguoiLienHe = contactPerson
                isPassengerValid = true
            }
        }
    }

    // Hàm lấy dữ liệu Hành lý
    @SuppressLint("SetTextI18n")
    private fun getLuggageData() {
        luggageViewModel = ViewModelProvider(this)[LuggageViewModel::class.java]

        tongHanhLy = 0
        // Observe changes to the contact person data
        luggageViewModel.selectedLuggageData.observe(this) { luggageData ->
            luggageData?.let {
                Log.d("Contact", "LuggageData $luggageData")
                tongHanhLy = luggageData.values
                    .flatten()
                    .sumOf { it.hanhLy.price }

                noteLuggage.text = "+${formatPrice(tongHanhLy)} VND"
                luggageList = luggageData
            }
            Log.d("Hành lý", "danh sách hành lý $luggageList")
            calculateTotalPrice(tongHanhLy)

//            flightBooking.hanhKhach = flightBooking.hanhKhach.map { passenger ->
//                val normalizedPassengerTitle = passenger.loaiHk.replace(Regex("\\d"), "").trim()
//                // Lọc hành lý phù hợp với passengerTitles và có cân nặng > 0
//                val matchingLuggage = luggageList.values.flatten()
//                    .filter { luggage ->
//                        luggage.passengerTitles == passenger.loaiHk
//                    }
//                    .map { it.hanhLy }
//                    .filter { it.weight > 0 }
////                val dvhl = listOf(luggaggeList.)
//                passenger.copy(
//                    loaiHk = normalizedPassengerTitle,
//                    dichVuHanhLy = passenger.dichVuHanhLy + matchingLuggage)
//            }

            

//            flightBooking.hanhKhach = flightBooking.hanhKhach.map { passenger ->
//                val normalizedPassengerTitle = passenger.loaiHk.replace(Regex("\\d"), "").trim()
//
//                // Lọc hành lý phù hợp với passengerTitles và có cân nặng > 0
//                val matchingLuggage = luggageList.values.flatten()
//                    .filter { luggage -> luggage.passengerTitles == passenger.loaiHk }
//                    .map { it.hanhLy }
//                    .filter { it.weight > 0 }
//
//                // Chuyển đổi DichVuHanhLy thành DVHL
//                val updatedDichVuHanhLy = passenger.dichVuHanhLy.map { luggage ->
//                    DVHL(
//                        soKy = luggage.weight.toString(),
//                        maChuyenBay = flightBooking.chuyenBay[0].maChuyenBay, // Mã chuyến bay lấy từ flightBooking
//                        maDVHL = luggage.serviceId
//                    )
//                }
//
//                passenger.copy(
//                    loaiHk = normalizedPassengerTitle,
//                    dichVuHanhLy = updatedDichVuHanhLy
//                )
//            }

//            validateInputs()
            btnContinue.setOnClickListener {
                setBookingData(flightBooking)
            }
        }
    }

    // Tính tổng tiền
    @SuppressLint("SetTextI18n")
    private fun calculateTotalPrice(priceLuggage: Long? = 0) {
        Log.d("Tien hanh ly", "Tien hanh ly $priceLuggage")
        tongTien = 0;

        val flightPrices = getFlightPrices()

        // Tính tổng tiền: Tổng giá vé * số lượng passengerTitles (không bao gồm trẻ sơ sinh)
        passengerTitles.forEach { title ->
            if (!title.lowercase().contains("trẻ sơ sinh", ignoreCase = true)) {
                flightPrices.forEach { giaVe ->
                    tongTien += giaVe
                }
            }
        }

        if (priceLuggage != null) {
            tongTien += priceLuggage
        }
        tvTongTien.text = "VND ${formatPrice(tongTien)}"
        labelTongTien.text = "Tổng giá tiền cho ${passengerTitles.size} người"
//        validateInputs()
    }

    // Hàm lấy giá vé của từng chuyến bay trong bookingList
    private fun getFlightPrices(): List<Long> {
        val flightPrices = mutableListOf<Long>()

        for (datCho in bookingList) {
            // Giả sử DatChoData có thuộc tính giaVe là giá vé
            flightPrices.add(datCho.goiDichVu.giaGoi)
        }

        Log.d("FlightPrices", "Giá vé từng chuyến bay: $flightPrices")
        return flightPrices
    }

    // Hàm format tiền
    fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it)
        } ?: "N/A"
    }

    // Hàm lấy dữ liệu chuyến bay cho flightBooking
    fun populateFlightBooking(bookingList: List<DatChoData>): ArrayList<Flight> {

        val flightList: ArrayList<Flight> = arrayListOf()
        for (booking in bookingList) {

            val validPassengerTitles = passengerTitles.filterNot { it.lowercase().contains("em bé", ignoreCase = true) }
            val soGheBus = if (booking.goiDichVu.tenGoi.lowercase().contains("bus", ignoreCase = true)) validPassengerTitles.size else 0
            val soGheEco = if (booking.goiDichVu.tenGoi.lowercase().contains("eco", ignoreCase = true)) validPassengerTitles.size else 0

            val flight = Flight(
                maChuyenBay = booking.chuyenBay.maChuyenBay,
                soGheBus = soGheBus,
                soGheEco = soGheEco,
                maGoi = booking.goiDichVu.maGoi.toIntOrNull() ?: 0
            )
            flightList.add(flight)
        }

        Log.d("CHUYENBAY", "CHUYENBAY $flightList")
        return flightList
    }

//    private fun hamCapNhat() {
//        for (booking in bookingList) {
//            // Lấy mã chuyến bay từ booking
//            val maChuyenBay = booking.chuyenBay.maChuyenBay
//
//            // Tìm dịch vụ hành lý tương ứng trong luggageList
//            val luggageForFlight = luggageList[0]
//            val luggageReturn = luggageList[1]
//
//
//            if (luggageForFlight != null) {
//                for (index in luggageForFlight.indices) {
//                    val hanhLyPassenger = luggageForFlight[index]
//                    val hanhLy = DVHL(
//                        soKy = hanhLyPassenger.hanhLy.weight.toString(), maChuyenBay = booking.chuyenBay.maChuyenBay,
//                        maDVHL = hanhLyPassenger.hanhLy.serviceId
//                    )
//                    flightBooking.hanhKhach[index].dichVuHanhLy.add(hanhLy)
//                }
//            }
//
//
//            if (luggageReturn != null) {
//                for (index in luggageReturn.indices) {
//                    val hanhLyPassenger = luggageReturn[index]
//                    val hanhLy = DVHL(
//                        soKy = hanhLyPassenger.hanhLy.weight.toString(), maChuyenBay = booking.chuyenBay.maChuyenBay,
//                        maDVHL = hanhLyPassenger.hanhLy.serviceId
//                    )
//                    flightBooking.hanhKhach[index].dichVuHanhLy.add(hanhLy)
//                }
//            }
//        }
//    }

        fun populateHanhKhach(passengerInfoList: List<PassengerInfo>): List<HanhKhach> {
            val hanhKhachList = mutableListOf<HanhKhach>()

            passengerTitles.forEachIndexed { index, passengerTitle ->

                // Tạo HanhKhach cho hành khách và gán dữ liệu vào
                val hanhKhach = HanhKhach(
                    hoHk = passengerInfoList.getOrNull(index)?.lastName ?: "N/A",
                    tenHk = passengerInfoList.getOrNull(index)?.firstName ?: "N/A",
                    danhXung = passengerInfoList.getOrNull(index)?.title ?: "Mr/Ms",
                    cccd = passengerInfoList.getOrNull(index)?.idNumber ?: "Unknown",
                    ngaySinh = passengerInfoList.getOrNull(index)?.birthDate ?: "01/01/1970",
                    quocTich = passengerInfoList.getOrNull(index)?.country ?: "Vietnam",
                    loaiHk = passengerTitle,
                    dichVuHanhLy = emptyList()
                )

                hanhKhachList.add(hanhKhach)
            }

            Log.d("HanhKhachList", "Danh sách hành khách: $hanhKhachList")
            return hanhKhachList
        }

        // Hàm gửi dữ liệu booking
        private fun setBookingData(flightBooking: FlightBooking) {
            val apiService = ApiClient.retrofit.create(ApiService::class.java)
            val call: Call<BookingResponse> = apiService.setBookingData(flightBooking)

            call.enqueue(object : Callback<BookingResponse> {
                override fun onResponse(
                    call: Call<BookingResponse>,
                    response: Response<BookingResponse>
                ) {
                    if (response.isSuccessful) {
                        val bookingResponse = response.body()
                        if (bookingResponse != null) {
                            // Xử lý dữ liệu thành công
                            Log.d("FlightBooking", "Booking successful: $bookingResponse")
                            Toast.makeText(
                                this@InfoAndLuggageActivity,
                                "Gửi dữ liệu thành công",
                                Toast.LENGTH_SHORT
                            ).show()
                            bookingResponseData = bookingResponse

                            Log.d("Debug", "DATA_BOOKING_RESPONSE: $bookingResponseData")
                            Log.d("Debug", "DATA_CHUYENBAY_GOIDICHVU: $bookingList")
                            Log.d("Debug", "TONG_TIEN: $tongTien")
                            Log.d("Debug", "TONG_TIEN_HANH_LY: $tongHanhLy")


                            val intent =
                                Intent(this@InfoAndLuggageActivity, ThanhToanActivity::class.java)
                            Log.d("Debug", "INTENT: $intent")

                            intent.putExtra("DATA_BOOKING_RESPONSE", bookingResponseData)
                            intent.putExtra("DATA_CHUYENBAY_GOIDICHVU", bookingList)
                            intent.putExtra("TONG_TIEN", tongTien)
                            intent.putExtra("TONG_TIEN_HANH_LY", tongHanhLy)
                            startActivity(intent)
                        }
                    } else {
                        Toast.makeText(
                            this@InfoAndLuggageActivity,
                            "Lỗi: ${response.message()}",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                }

                override fun onFailure(p0: Call<BookingResponse>, p1: Throwable) {
                    Toast.makeText(
                        this@InfoAndLuggageActivity,
                        "Lỗi kết nối: ${p1.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            })
        }

        private fun validateInputs() {
            val isContactPersonValid = tvContactPerson.text.isEmpty()
            val isLuggageValid = !noteLuggage.text.contains("Chưa")
            btnContinue.isEnabled = isContactPersonValid && isLuggageValid && isPassengerValid
        }

}