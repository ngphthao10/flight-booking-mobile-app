package com.example.datvemaybay.models;

import android.os.Parcel;
import android.os.Parcelable;
import androidx.annotation.NonNull;

public class HangHangKhongModel implements Parcelable {
    private String MaHHK;
    private String TenHHK;
    private String MaQG;

    public HangHangKhongModel(String maHHK, String tenHHK, String maQG) {
        MaHHK = maHHK;
        TenHHK = tenHHK;
        MaQG = maQG;
    }

    protected HangHangKhongModel(Parcel in) {
        MaHHK = in.readString();
        TenHHK = in.readString();
        MaQG = in.readString();
    }

    public static final Creator<HangHangKhongModel> CREATOR = new Creator<HangHangKhongModel>() {
        @Override
        public HangHangKhongModel createFromParcel(Parcel in) {
            return new HangHangKhongModel(in);
        }

        @Override
        public HangHangKhongModel[] newArray(int size) {
            return new HangHangKhongModel[size];
        }
    };

    public String getMaHHK() {
        return MaHHK;
    }

    public void setMaHHK(String maHHK) {
        MaHHK = maHHK;
    }

    public String getTenHHK() {
        return TenHHK;
    }

    public void setTenHHK(String tenHHK) {
        TenHHK = tenHHK;
    }

    public String getMaQG() {
        return MaQG;
    }

    public void setMaQG(String maQG) {
        MaQG = maQG;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(@NonNull Parcel parcel, int i) {
        parcel.writeString(MaHHK);
        parcel.writeString(TenHHK);
        parcel.writeString(MaQG);
    }
}
