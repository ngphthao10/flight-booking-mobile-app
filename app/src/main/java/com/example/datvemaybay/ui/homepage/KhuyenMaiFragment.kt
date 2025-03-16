package com.example.datvemaybay.ui.homepage

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.adapter.KhuyenMaiAdapter
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.HangHangKhongKhuyenMai
import com.example.datvemaybay.data.models.KhuyenMai
import com.example.datvemaybay.data.models.KhuyenMaiRequest
import com.example.datvemaybay.data.models.KhuyenMaiResponse
import com.example.datvemaybay.data.models.SanBayResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class KhuyenMaiFragment(private val khuyenMaiRequest: KhuyenMaiRequest) : Fragment() {

    private lateinit var listener: OnKhuyenMaiSelectedListener

    private lateinit var edtMaKhuyenMai: EditText
    private lateinit var rvCoupons: RecyclerView
    private lateinit var khuyenMaiAdapter: KhuyenMaiAdapter
    private val coupons = mutableListOf<HangHangKhongKhuyenMai>()
    private lateinit var btnApply: Button
    private lateinit var btnCancel: ImageButton

    interface OnKhuyenMaiSelectedListener {
        fun onKhuyenMaiSelected(coupon: HangHangKhongKhuyenMai)
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        if (context is OnKhuyenMaiSelectedListener) {
            listener = context
        } else {
            throw RuntimeException("$context must implement OnKhuyenMaiSelectedListener")
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_khuyen_mai, container, false)

        edtMaKhuyenMai = view.findViewById(R.id.edtMaKhuyenMai)
        rvCoupons = view.findViewById(R.id.rvCoupons)
        btnApply = view.findViewById(R.id.btnApply)

        khuyenMaiAdapter = KhuyenMaiAdapter(coupons, requireContext(), object : KhuyenMaiAdapter.OnCouponClickListener {
            override fun onCouponClick(coupon: HangHangKhongKhuyenMai) {
                listener.onKhuyenMaiSelected(coupon)
                parentFragmentManager.popBackStack()
            }
        })

        rvCoupons.layoutManager = LinearLayoutManager(requireContext())
        rvCoupons.adapter = khuyenMaiAdapter

        getKhuyenMaiPromotions(khuyenMaiRequest)

        btnCancel = view.findViewById(R.id.btnCancel)
        btnCancel.setOnClickListener {
            parentFragmentManager.popBackStack()
        }

        return view
    }

    private fun applyCoupon() {
        val couponCode = edtMaKhuyenMai.text.toString().trim()

        if (couponCode.isEmpty()) {
            Toast.makeText(requireContext(), "Vui lòng nhập mã khuyến mãi", Toast.LENGTH_SHORT).show()
            return
        }
    }

    private fun getKhuyenMaiPromotions(khuyenMaiRequest: KhuyenMaiRequest) {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val call: Call<KhuyenMaiResponse> = apiService.getKhuyenMaiPromotions(khuyenMaiRequest)

        call.enqueue(object : Callback<KhuyenMaiResponse> {
            override fun onResponse(call: Call<KhuyenMaiResponse>, response: Response<KhuyenMaiResponse>) {
                if (response.isSuccessful) {
                    val khuyenMaiResponse = response.body()
                    if (khuyenMaiResponse != null) {
                        // Cập nhật dữ liệu lên RecyclerView
                        khuyenMaiAdapter.updateCoupons(khuyenMaiResponse.khuyenMai.hangHangKhong)
                        Log.d("AirportAdapter", "Dữ liệu đã được cập nhật: " + khuyenMaiResponse.toString());
                    }
                } else {
                    Toast.makeText(requireContext(), "Lỗi: ${response.message()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<KhuyenMaiResponse>, t: Throwable) {
                Toast.makeText(requireContext(), "Lỗi kết nối: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
}

