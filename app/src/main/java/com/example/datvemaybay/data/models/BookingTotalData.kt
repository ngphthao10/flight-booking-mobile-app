import com.example.datvemaybay.data.models.ContactPerson
import com.example.datvemaybay.data.models.DichVuHanhLy
import com.google.gson.annotations.SerializedName
import java.io.Serializable

// Lớp dữ liệu chính
data class FlightBooking(
    @SerializedName("nguoi_lien_he") var nguoiLienHe: ContactPerson = ContactPerson(),
    @SerializedName("hanh_khach") var hanhKhach: List<HanhKhach> = emptyList(),
    @SerializedName("chuyen_bay") var chuyenBay: List<Flight> = emptyList()
) : Serializable

// Lớp dữ liệu cho hành khách
data class HanhKhach(
    @SerializedName("ho_hk") val hoHk: String,
    @SerializedName("ten_hk") val tenHk: String,
    @SerializedName("danh_xung") val danhXung: String,
    @SerializedName("cccd") val cccd: String,
    @SerializedName("ngay_sinh") val ngaySinh: String,
    @SerializedName("quoc_tich") val quocTich: String,
    @SerializedName("loai_hk") val loaiHk: String,
    @SerializedName("dich_vu_hanh_ly") var dichVuHanhLy: List<DichVuHanhLy> = arrayListOf()
): Serializable

data class DVHL(
    @SerializedName("so_ky") val soKy: String,
    @SerializedName("ma_chuyen_bay") val maChuyenBay: String,
    @SerializedName("ma_dich_vu_hanh_ly") val maDVHL: Int,
): Serializable

// Lớp dữ liệu cho chuyến bay
data class Flight(
    @SerializedName("ma_chuyen_bay") val maChuyenBay: String,
    @SerializedName("so_ghe_bus") val soGheBus: Int,
    @SerializedName("so_ghe_eco") val soGheEco: Int,
    @SerializedName("ma_goi") val maGoi: Int
): Serializable
