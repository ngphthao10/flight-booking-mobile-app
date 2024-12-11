package com.example.datvemaybay.response;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class HangHangKhongListResponse {

    @SerializedName("data")
    @Expose
    private List<DataItem> data;

    @SerializedName("filters")
    @Expose
    private Filters filters;

    @SerializedName("message")
    @Expose
    private String message;

    @SerializedName("pagination")
    @Expose
    private Pagination pagination;

    @SerializedName("status")
    @Expose
    private boolean status;

    // Getters and Setters
    public List<DataItem> getData() {
        return data;
    }

    public void setData(List<DataItem> data) {
        this.data = data;
    }

    public Filters getFilters() {
        return filters;
    }

    public void setFilters(Filters filters) {
        this.filters = filters;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Pagination getPagination() {
        return pagination;
    }

    public void setPagination(Pagination pagination) {
        this.pagination = pagination;
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    // Lớp con DataItem
    public static class DataItem {

        @SerializedName("MaHHK")
        @Expose
        private String maHHK;

        @SerializedName("MaQG")
        @Expose
        private String maQG;

        @SerializedName("TenHHK")
        @Expose
        private String tenHHK;

        public DataItem(String maHHK, String maQG, String tenHHK) {
            this.maHHK = maHHK;
            this.maQG = maQG;
            this.tenHHK = tenHHK;
        }
        // Getters and Setters
        public String getMaHHK() {
            return maHHK;
        }

        public void setMaHHK(String maHHK) {
            this.maHHK = maHHK;
        }

        public String getMaQG() {
            return maQG;
        }

        public void setMaQG(String maQG) {
            this.maQG = maQG;
        }

        public String getTenHHK() {
            return tenHHK;
        }

        public void setTenHHK(String tenHHK) {
            this.tenHHK = tenHHK;
        }
    }

    // Lớp con Filters
    public static class Filters {

        @SerializedName("ma_hhk")
        @Expose
        private String maHHK;

        @SerializedName("ma_qg")
        @Expose
        private String maQG;

        @SerializedName("order")
        @Expose
        private String order;

        @SerializedName("sort_by")
        @Expose
        private String sortBy;

        @SerializedName("ten_hhk")
        @Expose
        private String tenHHK;

        // Getters and Setters
        public String getMaHHK() {
            return maHHK;
        }

        public void setMaHHK(String maHHK) {
            this.maHHK = maHHK;
        }

        public String getMaQG() {
            return maQG;
        }

        public void setMaQG(String maQG) {
            this.maQG = maQG;
        }

        public String getOrder() {
            return order;
        }

        public void setOrder(String order) {
            this.order = order;
        }

        public String getSortBy() {
            return sortBy;
        }

        public void setSortBy(String sortBy) {
            this.sortBy = sortBy;
        }

        public String getTenHHK() {
            return tenHHK;
        }

        public void setTenHHK(String tenHHK) {
            this.tenHHK = tenHHK;
        }
    }

    // Lớp con Pagination
    public static class Pagination {

        @SerializedName("page")
        @Expose
        private int page;

        @SerializedName("pages")
        @Expose
        private int pages;

        @SerializedName("per_page")
        @Expose
        private int perPage;

        @SerializedName("total")
        @Expose
        private int total;

        // Getters and Setters
        public int getPage() {
            return page;
        }

        public void setPage(int page) {
            this.page = page;
        }

        public int getPages() {
            return pages;
        }

        public void setPages(int pages) {
            this.pages = pages;
        }

        public int getPerPage() {
            return perPage;
        }

        public void setPerPage(int perPage) {
            this.perPage = perPage;
        }

        public int getTotal() {
            return total;
        }

        public void setTotal(int total) {
            this.total = total;
        }
    }

    @Override
    public String toString() {
        return "HangHangKhongListResponse{" +
                "data=" + data +
                ", filters=" + filters +
                ", message='" + message + '\'' +
                ", pagination=" + pagination +
                ", status=" + status +
                '}';
    }
}
