package com.example.datvemaybay.data.models

import android.os.Parcel
import android.os.Parcelable
import com.google.gson.annotations.SerializedName
import java.io.Serializable

data class SanBay(
    @SerializedName("MaSanBay") val maSanBay: String,
    @SerializedName("TenSanBay") val tenSanBay: String,
    @SerializedName("ThanhPho") val thanhPho: String,
    @SerializedName("MaQG") val tenQG: String,
    @SerializedName("LoaiSB") val loaiSB: String
): Parcelable {

    constructor(parcel: Parcel) : this(
        parcel.readString() ?: "",
        parcel.readString() ?: "",
        parcel.readString() ?: "",
        parcel.readString() ?: "",
        parcel.readString() ?: ""
    )

    override fun writeToParcel(parcel: Parcel, flags: Int) {
        parcel.writeString(loaiSB)
        parcel.writeString(tenQG)
        parcel.writeString(maSanBay)
        parcel.writeString(tenSanBay)
        parcel.writeString(thanhPho)
    }

    override fun describeContents(): Int = 0

    companion object CREATOR : Parcelable.Creator<SanBay> {
        override fun createFromParcel(parcel: Parcel): SanBay {
            return SanBay(parcel)
        }

        override fun newArray(size: Int): Array<SanBay?> {
            return arrayOfNulls(size)
        }
    }
}

data class SanBayResponse(
    val status: Boolean,
    val message: String,
    val data: List<SanBay>
)