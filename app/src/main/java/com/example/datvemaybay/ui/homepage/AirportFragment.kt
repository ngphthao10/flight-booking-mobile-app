package com.example.datvemaybay.ui.homepage

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.adapter.AirportAdapter
import com.example.datvemaybay.data.models.SanBay

class AirportFragment : Fragment() {

    lateinit var recyclerView: RecyclerView
    lateinit var btnCancel: Button
    private lateinit var airportAdapter: AirportAdapter

    private var listener: OnItemSelectedListener? = null
    private var input: String? = null

    interface OnItemSelectedListener {
        fun onItemSelected(item: SanBay, input: String)
    }

    companion object {
        // Hàm khởi tạo Fragment với Adapter
        fun newInstance(adapter: AirportAdapter, input: String): AirportFragment {
            val fragment = AirportFragment()
            fragment.airportAdapter = adapter
            val bundle = Bundle()
            bundle.putString("input", input)
            fragment.arguments = bundle
            return fragment
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate layout
        val view = inflater.inflate(R.layout.fragment_san_bay, container, false)

        // Initialize RecyclerView
        recyclerView = view.findViewById(R.id.rvAirportList)
        recyclerView.layoutManager = LinearLayoutManager(requireContext())
        recyclerView.adapter = airportAdapter

        // Xử lý sự kiện của nút Cancel
        btnCancel = view.findViewById(R.id.btnCancel)
        btnCancel.setOnClickListener {
            requireActivity().supportFragmentManager.popBackStack()
        }

        return view
    }

    fun setDataToRecyclerView(data: List<SanBay>) {
        airportAdapter.setData(data)
    }

    private fun setupRecyclerView() {
        val adapter = AirportAdapter { item ->
            listener?.onItemSelected(item, "unknown")
        }
        recyclerView.adapter = adapter
    }

}
