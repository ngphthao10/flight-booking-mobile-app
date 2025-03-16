package com.example.datvemaybay.data.adapter

import android.annotation.SuppressLint
import android.content.Context
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.core.os.persistableBundleOf
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.datvemaybay.R
import com.example.datvemaybay.data.api.ApiClient
import com.example.datvemaybay.data.api.ApiService
import com.example.datvemaybay.data.models.ChuyenBay
import com.example.datvemaybay.data.models.DatChoData
import com.example.datvemaybay.data.models.DichVuHanhLy
import com.example.datvemaybay.data.models.DichVuHanhLyResponse
import com.example.datvemaybay.data.models.HanhLyPassenger
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class LuggageAdapter(
    private val context: Context,
    private val datChoPassengerList: Map<DatChoData, List<HanhLyPassenger>>,
    private val passengerTitles: ArrayList<String>,
    private val listener: PackageLuggageAdapter.OnTotalPriceChangeListener
) : RecyclerView.Adapter<LuggageAdapter.LuggageViewHolder>() {

    private val selectedLuggageList = mutableMapOf<Int, MutableList<HanhLyPassenger>>()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): LuggageViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_luggage_flight, parent, false)
        return LuggageViewHolder(view)
    }

    override fun onBindViewHolder(holder: LuggageViewHolder, position: Int) {
        // Chuyển Map thành List và truy cập phần tử theo vị trí
        val datChoPassenger = datChoPassengerList.entries.toList()[position]
        holder.bind(datChoPassenger, passengerTitles, position)
    }

    override fun getItemCount(): Int = datChoPassengerList.size

    inner class LuggageViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {

        private val flightInfo: TextView = itemView.findViewById(R.id.flight_info)
        private val rvPersonLuggage: RecyclerView = itemView.findViewById(R.id.rvPersonLuggage)

        @SuppressLint("SetTextI18n")
        fun bind(datChoPassenger: Map.Entry<DatChoData, List<HanhLyPassenger>>, passengerTitles: ArrayList<String>, position: Int) {
            // Hiển thị thông tin chuyến bay
            flightInfo.text = "${datChoPassenger.key.chuyenBay.sanBayDi} → ${datChoPassenger.key.chuyenBay.sanBayDen}"

//            getDichVuHanhLyChuyenBay(datChoPassenger.key.chuyenBay.maChuyenBay) { luggageList ->
//                luggageFlightList = luggageList
//                rvPersonLuggage.layoutManager = LinearLayoutManager(itemView.context)
//                rvPersonLuggage.adapter = PassengerLuggageAdapter(passengerTitles, luggageFlightList, listener)
//            }

            getDichVuHanhLyChuyenBay(datChoPassenger.key.chuyenBay.maChuyenBay) { luggageList ->
                rvPersonLuggage.layoutManager = LinearLayoutManager(itemView.context)
                rvPersonLuggage.adapter = PassengerLuggageAdapter(
                    passengerTitles, luggageList, listener
                ) { selectedLuggage ->
                    selectedLuggageList[position] = mutableListOf(selectedLuggage)
                }
            }
        }
    }

    // Lấy danh sách dịch vụ hành lý
    @SuppressLint("SetTextI18n")
    fun getDichVuHanhLyChuyenBay(flightID: String, onResult: (List<DichVuHanhLy>) -> Unit) {
        // Tạo dịch vụ hành lý mặc định 0kg, 0VND
        val defaultDichVuHanhLy = DichVuHanhLy(0, 0, "", 0)

        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        // Gửi yêu cầu
        apiService.getDichVuHanhLyChuyenBay(flightID).enqueue(object :
            Callback<DichVuHanhLyResponse> {
            @SuppressLint("SetTextI18n", "NotifyDataSetChanged")
            override fun onResponse(
                call: Call<DichVuHanhLyResponse>,
                response: Response<DichVuHanhLyResponse>
            ) {
                if (response.isSuccessful && response.body() != null) {
                    // Kết hợp dịch vụ hành lý mặc định với các dịch vụ từ API
                    val combinedList = mutableListOf(defaultDichVuHanhLy)
                    combinedList.addAll(response.body()!!.listDVHL)  // Thêm các dịch vụ từ API vào sau dịch vụ mặc định
                    onResult(combinedList)  // Trả về danh sách kết hợp
                } else {
                    Toast.makeText(
                        context,
                        "Lỗi: ${response.message()}",
                        Toast.LENGTH_SHORT
                    ).show()
                    onResult(emptyList())
                }
            }

            override fun onFailure(call: Call<DichVuHanhLyResponse>, t: Throwable) {
                Toast.makeText(context, "Lỗi kết nối: ${t.message}", Toast.LENGTH_SHORT).show()
                onResult(emptyList())
            }
        })
    }

    fun getSelectedLuggageData(): MutableMap<Int, MutableList<HanhLyPassenger>> {
        return selectedLuggageList
    }
}

