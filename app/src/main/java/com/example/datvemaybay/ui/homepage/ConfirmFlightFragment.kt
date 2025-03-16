package com.example.datvemaybay.ui.homepage

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import androidx.fragment.app.FragmentTransaction
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.adapter.ConfirmFlightAdapter
import com.example.datvemaybay.data.models.ChuyenBay
import java.text.DecimalFormat
import kotlin.math.roundToInt

class ConfirmFlightFragment : Fragment() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: ConfirmFlightAdapter
    private lateinit var tvTongGiaVe: TextView
    private lateinit var btnBack: ImageButton
    private lateinit var tvFromTo: TextView
    private lateinit var btnContinue: Button

    private val flights = mutableListOf<ChuyenBay>()
    val maChuyenBayList = ArrayList<String>()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_confirm_flight, container, false)

        // Khởi tạo RecyclerView
        recyclerView = view.findViewById(R.id.rvConfirmFlight)
        tvTongGiaVe = view.findViewById(R.id.tvTotalPrice)
        btnBack = view.findViewById(R.id.backButton)
        tvFromTo = view.findViewById(R.id.tvFromTo)
        btnContinue = view.findViewById(R.id.btnContinue)

        recyclerView.layoutManager = LinearLayoutManager(requireContext())
        adapter = ConfirmFlightAdapter(flights)
        recyclerView.adapter = adapter

        // Lấy dữ liệu chuyến bay từ arguments
        loadFlightsFromArguments()

        // Xử lý sự kiện của nút Back
        btnBack.setOnClickListener {
            requireActivity().supportFragmentManager.popBackStack()
        }

        // Thêm tất cả mã chuyến bay vào danh sách
        flights.forEach { flight ->
            maChuyenBayList.add(flight.maChuyenBay)
        }

        // Xử lý sự kiện click nút Continue
        btnContinue.setOnClickListener {
            if (flights.isNotEmpty()) {
                navigateToPackageFragment(0)
            }
        }

        return view
    }

    @SuppressLint("NotifyDataSetChanged", "SetTextI18n")
    private fun loadFlightsFromArguments() {
        val receivedFlights = arguments?.getSerializable("FLIGHT_LIST") as? ArrayList<ChuyenBay>
        Log.d("Dữ liệu", "Danh sách chuyến bay: $receivedFlights" )
        if (receivedFlights != null) {
            flights.clear()
            flights.addAll(receivedFlights)
            adapter.notifyDataSetChanged()

            val tongGiaVe = flights.sumOf { flight ->
                when (flight.loaiGhe.lowercase()) {
                    "eco" -> flight.giaVeEco
                    "bus" -> flight.giaVeBus
                    else -> 0
                }
            }
            tvTongGiaVe.text = "VND ${formatPrice(tongGiaVe)}"
            if (receivedFlights.count() == 1) {
                tvFromTo.text = "${flights[0].sanBayDi} → ${flights[0].sanBayDen}"
            }
            else if (receivedFlights.count() == 2) {
                tvFromTo.text = "${flights[0].sanBayDi} ⇌ ${flights[0].sanBayDen}"
            }
        } else {
            tvTongGiaVe.text = "Không có chuyến bay nào!"
        }
    }

    // Hàm chuyển hướng đến fragment khác
    private fun navigateToPackageFragment(index: Int) {
        val flight = flights[index]

        val bundle = Bundle().apply {
            putSerializable("flights", ArrayList(flights))
            putInt("current_index", index)
            putInt("total_flights", flights.size)
        }

        val fragment = PackageFragment().apply {
            arguments = bundle
        }

        requireActivity().supportFragmentManager.beginTransaction()
            .replace(android.R.id.content, fragment)
            .addToBackStack(null)
            .commit()
    }

    // Hàm format tiền
    private fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it)
        } ?: "N/A"
    }
}