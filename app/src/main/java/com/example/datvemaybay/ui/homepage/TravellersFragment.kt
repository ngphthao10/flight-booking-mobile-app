package com.example.datvemaybay.ui.homepage

import android.annotation.SuppressLint
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.databinding.FragmentTravellersBinding
import com.google.android.material.bottomsheet.BottomSheetDialogFragment

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [TravellersFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class TravellersFragment() : BottomSheetDialogFragment() {
    private lateinit var recyclerView: RecyclerView
    private var adultCount: Int = 0
    private var childCount: Int = 0
    private var infantCount: Int = 0

    private lateinit var txtAdultCount: TextView
    private lateinit var txtChildCount: TextView
    private lateinit var txtInfantCount: TextView

    private lateinit var btnMinusAdult: Button
    private lateinit var btnPlusAdult: Button
    private lateinit var btnMinusChild: Button
    private lateinit var btnPlusChild: Button
    private lateinit var btnMinusInfant: Button
    private lateinit var btnPlusInfant: Button

    private lateinit var btnCancel: Button
    private lateinit var btnSelect: Button

    companion object {
        fun newInstance(adultCount: Int, childCount: Int, infantCount: Int): TravellersFragment {
            val fragment = TravellersFragment()
            val args = Bundle()
            args.putInt("adult_count", adultCount)
            args.putInt("child_count", childCount)
            args.putInt("infant_count", infantCount)
            fragment.arguments = args
            return fragment
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            adultCount = it.getInt("adult_count", 1)
            childCount = it.getInt("child_count", 0)
            infantCount = it.getInt("infant_count", 0)
        }
    }

    @SuppressLint("SetTextI18n")
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val view = inflater.inflate(R.layout.fragment_travellers, container, false)
        val binding = FragmentTravellersBinding.inflate(inflater, container, false)

        txtAdultCount = binding.txtAdultCount
        txtChildCount = binding.txtChildCount
        txtInfantCount = binding.txtInfantCount

        btnMinusAdult = binding.btnMinusAdult
        btnPlusAdult = binding.btnPlusAdult
        btnMinusChild = binding.btnMinusChild
        btnPlusChild = binding.btnPlusChild
        btnMinusInfant = binding.btnMinusInfant
        btnPlusInfant = binding.btnPlusInfant

        btnCancel = binding.btnCancel
        btnSelect = binding.btnSelect

        updateTravellerCounts()

        // Xử lý tăng/ giảm số lượng hành khách
        ascendingDescendingCount()

        // Xử lý nút "Hủy"
        btnCancel.setOnClickListener {
            dismiss() // Đóng Fragment
        }

        // Xử lý nút "Chọn"
        btnSelect.setOnClickListener {
            val result = Bundle().apply {
                putString("adult_count", adultCount.toString())
                putString("child_count", childCount.toString())
                putString("infant_count", infantCount.toString())
            }
            parentFragmentManager.setFragmentResult("travellers_result", result)
            dismiss()
        }

        return binding.root
    }

    // Hàm cập nhật giao diện số lượng hành khách
    @SuppressLint("SetTextI18n")
    private fun updateTravellerCounts() {
        txtAdultCount.text = adultCount.toString()
        txtChildCount.text = childCount.toString()
        txtInfantCount.text = infantCount.toString()
    }

    // Hàm xử lý tăng giảm cho các nút
    private fun ascendingDescendingCount() {
        // Xử lý nút tăng/giảm cho người lớn
        btnPlusAdult.setOnClickListener {
            adultCount++
            updateTravellerCounts()
        }

        btnMinusAdult.setOnClickListener {
            if (adultCount > 1) {
                adultCount--
                updateTravellerCounts()
            }
        }

        // Xử lý nút tăng/giảm cho trẻ em
        btnPlusChild.setOnClickListener {
            childCount++
            updateTravellerCounts()
        }

        btnMinusChild.setOnClickListener {
            if (childCount > 0) {
                childCount--
                updateTravellerCounts()
            }
        }

        // Xử lý nút tăng/giảm cho em bé
        btnPlusInfant.setOnClickListener {
            infantCount++
            updateTravellerCounts()
        }

        btnMinusInfant.setOnClickListener {
            if (infantCount > 0) {
                infantCount--
                updateTravellerCounts()
            }
        }

        // Xử lý nút "Hủy"
        btnCancel.setOnClickListener {
            dismiss() // Đóng Fragment
        }
    }
}