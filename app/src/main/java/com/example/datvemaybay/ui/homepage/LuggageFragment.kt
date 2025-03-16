package com.example.datvemaybay.ui.homepage

import android.annotation.SuppressLint
import android.content.Context
import android.content.SharedPreferences
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
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.adapter.LuggageAdapter
import com.example.datvemaybay.data.adapter.PackageLuggageAdapter
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.DatChoData
import com.example.datvemaybay.data.models.DichVuHanhLy
import com.example.datvemaybay.data.models.DichVuHanhLyResponse
import com.example.datvemaybay.data.models.HanhLyPassenger
import com.example.datvemaybay.data.viewmodel.ContactPersonViewModel
import com.example.datvemaybay.data.viewmodel.LuggageViewModel
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.text.DecimalFormat

class LuggageFragment : Fragment(), PackageLuggageAdapter.OnTotalPriceChangeListener {

    private lateinit var luggageAdapter: LuggageAdapter
    private lateinit var rvLuggage: RecyclerView
    private lateinit var btnCancel: ImageButton

    private var bookingList: ArrayList<DatChoData>? = null
    private var passengerTitles: ArrayList<String>? = null

    private lateinit var viewModel: LuggageViewModel


    companion object {
        private const val ARG_BOOKING_LIST = "booking_list"
        private const val ARG_PASSENGER_TITLES = "passenger_titles"

        fun newInstance(
            bookingList: ArrayList<DatChoData>,
            passengerTitles: ArrayList<String>
        ): LuggageFragment {
            val fragment = LuggageFragment()
            val bundle = Bundle().apply {
                putSerializable(ARG_BOOKING_LIST, bookingList)
                putStringArrayList(ARG_PASSENGER_TITLES, passengerTitles)
            }
            fragment.arguments = bundle
            return fragment
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            bookingList = it.getSerializable(ARG_BOOKING_LIST) as? ArrayList<DatChoData>
            passengerTitles = it.getStringArrayList(ARG_PASSENGER_TITLES)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_luggage, container, false)

        viewModel = ViewModelProvider(requireActivity())[LuggageViewModel::class.java]

        // Khởi tạo RecyclerView và Adapter
        rvLuggage = view.findViewById(R.id.recyclerView)
        val btnSave = view.findViewById<Button>(R.id.saveButton)

        val datChoPassengerList: Map<DatChoData, List<HanhLyPassenger>> =
            bookingList?.toList()?.associateWith {
                emptyList<HanhLyPassenger>()
            } ?: emptyMap()

        luggageAdapter =
            passengerTitles?.let {
                LuggageAdapter(
                    requireContext(),
                    datChoPassengerList,
                    it,
                    this
                )
            }!!
        rvLuggage.layoutManager = LinearLayoutManager(requireContext())
        rvLuggage.adapter = luggageAdapter
        Log.d("LUGGAGEFRAGMENT", "LUGGAGEFRAGMENT $passengerTitles")

        btnSave.setOnClickListener {
            sendDataToActivity()
            parentFragmentManager.popBackStack()
        }

        btnCancel = view.findViewById(R.id.back_button)
        btnCancel.setOnClickListener() {
            parentFragmentManager.popBackStack()
        }
        return view
    }

    @SuppressLint("SetTextI18n")
    override fun onTotalPriceChanged(totalPrice: Long) {
        val sharedPreferences: SharedPreferences = requireContext().getSharedPreferences("LuggagePrefs", Context.MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        editor.putLong("TOTAL_PRICE_LUGGAGE", totalPrice)
        editor.apply()
        view?.findViewById<TextView>(R.id.totalTextView)?.text =
            "Tổng: \nVND ${formatPrice(totalPrice)}"
    }

    fun sendDataToActivity() {
        val selectedLuggageData = luggageAdapter.getSelectedLuggageData()
        viewModel.setSelectedLuggageData(selectedLuggageData)
        Log.d("dữ liệu hành lý", "dữ liệu hành lý $selectedLuggageData")
        Toast.makeText(context, "Lưu dữ liệu thành công", Toast.LENGTH_SHORT).show()
    }

    // Hàm format tiền
    fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it)
        } ?: "N/A"
    }
}