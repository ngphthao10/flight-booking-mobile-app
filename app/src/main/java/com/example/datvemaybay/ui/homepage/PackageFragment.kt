package com.example.datvemaybay.ui.homepage

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.cardview.widget.CardView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.InfoAndLuggageActivity
import com.example.datvemaybay.R
import com.example.datvemaybay.data.adapter.ServiceAdapter
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.ChuyenBay
import com.example.datvemaybay.data.models.ChuyenBayServiceResponse
import com.example.datvemaybay.data.models.DatChoData
import com.example.datvemaybay.data.models.DichVu
import com.example.datvemaybay.data.models.GoiDichVu
import com.example.datvemaybay.data.models.LoaiGheRequest
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.text.DecimalFormat

class PackageFragment : Fragment() {

    private lateinit var flights: ArrayList<ChuyenBay>
    private lateinit var bookingList: ArrayList<DatChoData>

    private var flightPackage: Map<String, GoiDichVu> = emptyMap()
    private var currentIndex: Int = 0
    private var totalFlights: Int = 0
    private lateinit var recyclerViewClass: RecyclerView
    private lateinit var recyclerViewPlus: RecyclerView
    private lateinit var serviceAdapter: ServiceAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Nhận dữ liệu chuyến bay
        flights = arguments?.getSerializable("flights") as ArrayList<ChuyenBay>
        currentIndex = arguments?.getInt("current_index", 0) ?: 0
        totalFlights = arguments?.getInt("total_flights", 1) ?: 1
        bookingList = (arguments?.getSerializable("bookingList") as? ArrayList<DatChoData>) ?: ArrayList()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_package, container, false)

        // fetch dữ liệu các gói dịch vụ của chuyến bay
        fetchServices(flights[currentIndex])

        // Hiển thị thông tin chuyến bay trên giao diện
        displayFlightDetails(view, flights[currentIndex])

        // Xử lý khi người dùng chọn CardView
        val btnClass = view.findViewById<Button>(R.id.btnChooseClass)
        val btnPlus = view.findViewById<Button>(R.id.btnChoosePlus)

//        val lastChoice = flightPackage.entries.lastOrNull()?.value
//        val firstChoice = flightPackage.entries.firstOrNull()?.value
//        if (firstChoice != null && lastChoice != null) {
//            clickOnCardView(btnClass, firstChoice)
//            clickOnCardView(btnPlus, lastChoice)
//        }

        // Xử lý sự kiện khi bấm nút back
        view.findViewById<ImageButton>(R.id.backButton).setOnClickListener {
            requireActivity().supportFragmentManager.popBackStack()
        }

        return view
    }

    private fun fetchServices(flight: ChuyenBay) {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val request = LoaiGheRequest(flight.loaiGhe)

        apiService.getChuyenBayService(flight.maChuyenBay, request).enqueue(object : Callback<ChuyenBayServiceResponse> {
            @SuppressLint("SetTextI18n")
            override fun onResponse(call: Call<ChuyenBayServiceResponse>, response: Response<ChuyenBayServiceResponse>) {
                if (response.isSuccessful) {
                    val chuyenBayServiceResponse = response.body()
                    if (chuyenBayServiceResponse != null) {
                        // Nhận dữ liệu của gói dịch vụ
                        flightPackage = chuyenBayServiceResponse.goiDichVu

                        // Thiết lập sự kiện khi đã có dữ liệu
                        val firstChoice = flightPackage.entries.firstOrNull()?.value
                        val lastChoice = flightPackage.entries.lastOrNull()?.value
                        if (firstChoice != null && lastChoice != null) {
                            clickOnCardView(view?.findViewById(R.id.btnChooseClass)!!, firstChoice)
                            clickOnCardView(view?.findViewById(R.id.btnChoosePlus)!!, lastChoice)
                        }

                        flightPackage.entries.firstOrNull()?.value?.let {
                            updateServiceList(
                                it.dichVu, recyclerViewClass)
                        }

                        flightPackage.entries.lastOrNull()?.value?.let {
                            updateServiceList(
                                it.dichVu, recyclerViewPlus)
                        }
                        Log.d("Response", "Dữ liệu gói dịch vụ: $flightPackage")
                    }
                    else {
                        Log.d("Response", "Đây là thông báo debug")
                    }
                } else {
                    Toast.makeText(requireContext(), "Lỗi: ${response.message()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<ChuyenBayServiceResponse>, t: Throwable) {
                Toast.makeText(requireContext(), "Lỗi kết nối: ${t.message}", Toast.LENGTH_SHORT).show()
            }

        })
    }

    // Hàm hiển thị thông tin lên giao diện
    @SuppressLint("SetTextI18n")
    private fun displayFlightDetails(view: View, flight: ChuyenBay) {
        // Tiêu để
        if (currentIndex + 1 == totalFlights) {
            view.findViewById<TextView>(R.id.title).text = "Chọn loại vé (Chuyến về)"
            view.findViewById<TextView>(R.id.tvLoaiChuyen).text = "Chuyến về"
        }

        // Khởi tạo RecyclerView
        recyclerViewClass = view.findViewById(R.id.recyclerViewClass)
        recyclerViewClass.layoutManager = LinearLayoutManager(requireContext())

        recyclerViewPlus = view.findViewById(R.id.recyclerViewPlus)
        recyclerViewPlus.layoutManager = LinearLayoutManager(requireContext())

        // Lấy thông tin gói dịch vụ của chuyến bay
        val lastChoice = flightPackage.entries.lastOrNull()?.value
        val firstChoice = flightPackage.entries.firstOrNull()?.value

        // Thông tin chuyến bay
        view.findViewById<TextView>(R.id.tvFromTo).text = "${flight.sanBayDi} → ${flight.sanBayDen}"

        // Thông tin package class
        if (firstChoice != null) {
            view.findViewById<TextView>(R.id.titleClass).text = firstChoice.tenGoi
            view.findViewById<TextView>(R.id.tvExtraPriceClass).text = "${formatPrice(firstChoice.giaGoi)} VND/khách"
        }

        // Thông tin package plus
        if (lastChoice != null) {
            view.findViewById<TextView>(R.id.titleClass).text = lastChoice.tenGoi
            view.findViewById<TextView>(R.id.tvExtraPriceClass).text = "${formatPrice(lastChoice.giaGoi)} VND/khách"
        }
    }

    // Hàm chuyển hướng đến fragment_package của chuyến bay trong list
    private fun navigateToNextPackageFragment() {

        val bundle = Bundle().apply {
            putSerializable("flights", flights)
            putInt("current_index", currentIndex + 1)
            putInt("total_flights", totalFlights)
            putSerializable("bookingList", bookingList)
        }

        val fragment = PackageFragment().apply {
            arguments = bundle
        }

        requireActivity().supportFragmentManager.beginTransaction()
            .replace(android.R.id.content, fragment)
            .addToBackStack(null)
            .commit()
    }

    // Cập nhật dữ liệu vào Adapter
    fun updateServiceList(listGoiDichVu: List<DichVu>, recyclerView: RecyclerView) {
        serviceAdapter = ServiceAdapter(listGoiDichVu)
        recyclerView.adapter = serviceAdapter
    }

    // Hàm format tiền
    private fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it)
        } ?: "N/A"
    }

    // Hàm xử lý khi người dùng bấm chọn 1 cardview
    private fun clickOnCardView(button: Button, selectedPackage: GoiDichVu) {
        Log.d("Chay đi", "Chạy đi")
        button.setOnClickListener {
            val existingBookingItemIndex = bookingList.indexOfFirst { it.chuyenBay == flights[currentIndex] }

            if (existingBookingItemIndex != -1) {
                bookingList[existingBookingItemIndex].goiDichVu = selectedPackage
//                Toast.makeText(requireContext(), "Cập nhật gói dịch vụ cho chuyến bay.", Toast.LENGTH_SHORT).show()
            } else {
                val bookingItem = DatChoData(flights[currentIndex], selectedPackage)
                bookingList.add(bookingItem)
//                Toast.makeText(requireContext(), "Thêm mới chuyến bay với gói dịch vụ.", Toast.LENGTH_SHORT).show()
            }

            if (currentIndex + 1 < totalFlights) {
                navigateToNextPackageFragment()
            } else {
                // Xử lý hoàn tất nếu đây là chuyến bay cuối cùng
                val intent = Intent(requireContext(), InfoAndLuggageActivity::class.java)
                intent.putExtra("BOOKING_DATA", bookingList)
                Log.d("DT", "dANH SÁCH ĐẶT CHỖ $bookingList")
                startActivity(intent)
                requireActivity().overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out)
            }
        }
    }
}
