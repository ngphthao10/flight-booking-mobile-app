// src/main/java/com/example/datvemaybay/HangHangKhongListActivity.kt

package com.example.datvemaybay

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.datvemaybay.adapter.HangHangKhongAdapter
import com.example.datvemaybay.api.ApiClient
import com.example.datvemaybay.api.ApiService
import com.example.datvemaybay.databinding.DialogAddHhkBinding
import com.example.datvemaybay.databinding.ActivityMainBinding
import com.example.datvemaybay.response.AddHHKResponse
import com.example.datvemaybay.response.HangHangKhongListResponse
import com.example.datvemaybay.response.QuocGia
import com.example.datvemaybay.response.QuocGiaResponse
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.snackbar.Snackbar
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import android.widget.ArrayAdapter
import android.widget.Toast
import com.google.android.material.textfield.TextInputLayout

class HangHangKhongListActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var adapter: HangHangKhongAdapter
    private var quocGiaList: List<QuocGia> = listOf()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        // Khởi tạo View Binding
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Khởi tạo RecyclerView
        binding.recyclerViewHangHK.layoutManager = LinearLayoutManager(this)
        adapter = HangHangKhongAdapter(mutableListOf())
        binding.recyclerViewHangHK.adapter = adapter

        // Khởi tạo FloatingActionButton
        binding.fabAddHHK.setOnClickListener {
            showAddHHKDialog()
        }

        // Gọi API để lấy danh sách hãng hàng không
        fetchHangHangKhongList()
    }

    private fun fetchHangHangKhongList() {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val call = apiService.getHangHangKhongList()

        call.enqueue(object : Callback<HangHangKhongListResponse> {
            override fun onResponse(
                call: Call<HangHangKhongListResponse>,
                response: Response<HangHangKhongListResponse>
            ) {
                if (response.isSuccessful && response.body() != null) {
                    val hangHangKhongListResponse = response.body()!!
                    if (hangHangKhongListResponse.isStatus()) {
                        val hangList = hangHangKhongListResponse.data
                        if (hangList != null) {
                            adapter.updateData(hangList)
                        } else {
                            Snackbar.make(binding.root, "Không có dữ liệu", Snackbar.LENGTH_LONG).show()
                        }
                    } else {
                        Snackbar.make(binding.root, "Lấy dữ liệu thất bại", Snackbar.LENGTH_LONG).show()
                    }
                } else {
                    Snackbar.make(binding.root, "Lỗi: ${response.code()}", Snackbar.LENGTH_LONG).show()
                }
            }

            override fun onFailure(call: Call<HangHangKhongListResponse>, t: Throwable) {
                Log.e("API_ERROR", "Lỗi mạng: ${t.message}")
                Snackbar.make(binding.root, "Lỗi mạng: ${t.message}", Snackbar.LENGTH_INDEFINITE)
                    .setAction("Thử lại") {
                        fetchHangHangKhongList()
                    }
                    .show()
            }
        })
    }

    private fun showAddHHKDialog() {
        // Khởi tạo View Binding cho dialog
        val dialogBinding = DialogAddHhkBinding.inflate(LayoutInflater.from(this))

        // Tạo dialog
        val dialog = MaterialAlertDialogBuilder(this)
            .setTitle("Thêm Hãng Hàng Không")
            .setView(dialogBinding.root)
            .setPositiveButton("Thêm", null) // Để override onClick sau
            .setNegativeButton("Hủy") { dialogInterface, _ ->
                dialogInterface.dismiss()
            }
            .create()

        dialog.setOnShowListener {
            // Gọi API để lấy danh sách quốc gia
            fetchQuocGiaList(dialogBinding)

            // Xử lý nút "Thêm" khi người dùng nhấn
            val buttonAdd = dialog.getButton(AlertDialog.BUTTON_POSITIVE)
            buttonAdd.setOnClickListener {
                val maHHK = dialogBinding.etMaHHK.text.toString().trim()
                val tenHHK = dialogBinding.etTenHHK.text.toString().trim()
                val selectedTenQG = dialogBinding.etMaQG.text.toString().trim()

                // Kiểm tra dữ liệu nhập
                var isValid = true
                if (maHHK.isEmpty()) {
                    dialogBinding.tilMaHHK.error = "Vui lòng nhập mã hãng hàng không"
                    isValid = false
                } else {
                    dialogBinding.tilMaHHK.error = null
                }

                if (tenHHK.isEmpty()) {
                    dialogBinding.tilTenHHK.error = "Vui lòng nhập tên hãng hàng không"
                    isValid = false
                } else {
                    dialogBinding.tilTenHHK.error = null
                }

                if (selectedTenQG.isEmpty()) {
                    dialogBinding.tilMaQG.error = "Vui lòng chọn quốc gia"
                    isValid = false
                } else {
                    dialogBinding.tilMaQG.error = null
                }

                if (!isValid) return@setOnClickListener

                // Tìm MaQG tương ứng với TenQG được chọn
                val selectedQuocGia = quocGiaList.find { it.tenQG == selectedTenQG }
                val maQG = selectedQuocGia?.maQG ?: ""

                // Kiểm tra lại MaQG
                if (maQG.isEmpty()) {
                    dialogBinding.tilMaQG.error = "Quốc gia không hợp lệ"
                    return@setOnClickListener
                }

                // Tạo đối tượng DataItem mới
                val newHHK = HangHangKhongListResponse.DataItem(
                    maHHK,maQG,tenHHK
                )

                // Gọi API để thêm mới hãng hàng không
                addHangHangKhong(newHHK, dialog)
            }
        }

        dialog.show()
    }

    private fun fetchQuocGiaList(dialogBinding: DialogAddHhkBinding) {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val call = apiService.getQuocGiaList()

        call.enqueue(object : Callback<QuocGiaResponse> {
            override fun onResponse(
                call: Call<QuocGiaResponse>,
                response: Response<QuocGiaResponse>
            ) {
                if (response.isSuccessful && response.body() != null) {
                    val quocGiaResponse = response.body()!!
                    if (quocGiaResponse.status) {
                        quocGiaList = quocGiaResponse.data ?: listOf()
                        val tenQuocGiaList = quocGiaList.map { it.tenQG }

                        // Thiết lập ArrayAdapter cho AutoCompleteTextView
                        val adapter = ArrayAdapter(
                            this@HangHangKhongListActivity,
                            android.R.layout.simple_dropdown_item_1line,
                            tenQuocGiaList
                        )
                        dialogBinding.etMaQG.setAdapter(adapter)
                    } else {
                        Snackbar.make(binding.root, "Lấy danh sách quốc gia thất bại", Snackbar.LENGTH_LONG).show()
                    }
                } else {
                    Snackbar.make(binding.root, "Lỗi: ${response.code()}", Snackbar.LENGTH_LONG).show()
                }
            }

            override fun onFailure(call: Call<QuocGiaResponse>, t: Throwable) {
                Log.e("API_ERROR", "Lỗi mạng khi lấy quốc gia: ${t.message}")
                Snackbar.make(binding.root, "Lỗi mạng khi lấy quốc gia: ${t.message}", Snackbar.LENGTH_LONG).show()
            }
        })
    }

    private fun addHangHangKhong(newHHK: HangHangKhongListResponse.DataItem, dialog: AlertDialog) {
        val apiService = ApiClient.retrofit.create(ApiService::class.java)
        val call = apiService.addHangHangKhong(newHHK)

        call.enqueue(object : Callback<AddHHKResponse> {
            override fun onResponse(
                call: Call<AddHHKResponse>,
                response: Response<AddHHKResponse>
            ) {
                if (response.isSuccessful && response.body() != null) {
                    val addResponse = response.body()!!
                    if (addResponse.status) {
                        // Thêm thành công, cập nhật RecyclerView
                        adapter.addItem(newHHK)
                        Snackbar.make(binding.root, "Thêm hãng hàng không thành công", Snackbar.LENGTH_LONG).show()
                        dialog.dismiss()
                    } else {
                        showErrorDialog("Thêm hãng hàng không thất bại: ${addResponse.message}")
                    }
                } else {
                    showErrorDialog("Lỗi: ${response.code()}")
                }
            }

            override fun onFailure(call: Call<AddHHKResponse>, t: Throwable) {
                Log.e("API_ERROR", "Lỗi mạng khi thêm: ${t.message}")
                showErrorDialog("Lỗi mạng khi thêm: ${t.message}")
            }
        })
    }

    private fun showErrorDialog(message: String) {
        AlertDialog.Builder(this)
            .setTitle("Lỗi")
            .setMessage(message)
            .setPositiveButton("OK") { dialogInterface, _ ->
                dialogInterface.dismiss()
            }
            .show()
    }

    // Giả sử phương thức enableEdgeToEdge được định nghĩa ở đây hoặc thông qua thư viện
    private fun enableEdgeToEdge() {
        // Implement edge-to-edge functionality nếu cần
    }
}
