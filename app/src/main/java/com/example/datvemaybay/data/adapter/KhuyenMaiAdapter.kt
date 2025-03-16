package com.example.datvemaybay.data.adapter

import android.annotation.SuppressLint
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.models.HangHangKhongKhuyenMai
import com.example.datvemaybay.data.models.KhuyenMai
import java.text.DecimalFormat

class KhuyenMaiAdapter(
    private var couponList: List<HangHangKhongKhuyenMai>,
    private val context: Context,
    private val listener: OnCouponClickListener
) : RecyclerView.Adapter<KhuyenMaiAdapter.KhuyenMaiViewHolder>() {

    interface OnCouponClickListener {
        fun onCouponClick(coupon: HangHangKhongKhuyenMai)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): KhuyenMaiViewHolder {
        val view = LayoutInflater.from(context).inflate(R.layout.item_khuyen_mai, parent, false)
        return KhuyenMaiViewHolder(view)
    }

    @SuppressLint("SetTextI18n")
    override fun onBindViewHolder(holder: KhuyenMaiViewHolder, position: Int) {
        val coupon = couponList[position]
        holder.tvTitle.text = coupon.tenKhuyenMai
        holder.tvMoTa.text = coupon.moTa
        holder.tvChiTiet.text = "Giảm ${formatPrice(coupon.tienGiam)} VND cho ${coupon.apDungCho}"

        // Handle item click
        holder.itemView.setOnClickListener {
            listener.onCouponClick(coupon)
        }
    }

    override fun getItemCount(): Int {
        return couponList.size
    }

    @SuppressLint("NotifyDataSetChanged")
    fun updateCoupons(newCoupons: List<HangHangKhongKhuyenMai>) {
        couponList = newCoupons
        notifyDataSetChanged()
    }

    inner class KhuyenMaiViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvTitle: TextView = itemView.findViewById(R.id.titleKhuyenMai)
        val tvMoTa: TextView = itemView.findViewById(R.id.tvMoTa)
        val tvChiTiet: TextView = itemView.findViewById(R.id.tvChiTiet)
    }

    // Hàm format tiền
    fun formatPrice(giaVe: Long?): String {
        return giaVe?.let {
            val formatter = DecimalFormat("#,###")
            formatter.format(it)
        } ?: "N/A"
    }
}
