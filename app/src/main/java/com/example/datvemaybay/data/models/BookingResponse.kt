import com.example.datvemaybay.data.models.DichVuHanhLy
import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class BookingResponse(
    @SerializedName("booking_id") val bookingId: String,
    @SerializedName("expires_in") val expiresIn: Int,
    @SerializedName("thong_tin_dat_cho") val thongTinDatCho: ThongTinDatCho
): Serializable

data class ThongTinDatCho(
    @SerializedName("chuyen_bay") val chuyenBay: List<ChuyenBay>,
    @SerializedName("flight_updates") val flightUpdates: Map<String, FlightUpdate>,
    @SerializedName("hanh_khach") val hanhKhach: List<HanhKhachResponse>,
    @SerializedName("nguoi_lien_he") val nguoiLienHe: NguoiLienHe
): Serializable

data class HanhKhachResponse (
    @SerializedName("ho_ten") val hoTen: String,
    @SerializedName("danh_xung") val danhXung: String,
    @SerializedName("cccd") val cccd: String,
    @SerializedName("ngay_sinh") val ngaySinh: String,
    @SerializedName("quoc_tich") val quocTich: String,
    @SerializedName("loai_hk") val loaiHk: String,
) : Serializable

data class ChuyenBay(
    @SerializedName("ma_chuyen_bay") val maChuyenBay: String,
    @SerializedName("ma_goi") val maGoi: Int,
    @SerializedName("so_ghe_bus") val soGheBus: Int,
    @SerializedName("so_ghe_eco") val soGheEco: Int
): Serializable

data class FlightUpdate(
    @SerializedName("SLBusConLai") val slBusConLai: Int,
    @SerializedName("SLEcoConLai") val slEcoConLai: Int,
    @SerializedName("ma_hhk") val maHhk: String
): Serializable


data class NguoiLienHe(
    @SerializedName("email") val email: String,
    @SerializedName("ho_ten") val hoTen: String,
    @SerializedName("sdt") val sdt: String
): Serializable
