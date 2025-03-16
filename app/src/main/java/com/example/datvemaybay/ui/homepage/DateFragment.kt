package com.example.datvemaybay.ui.homepage

import android.icu.text.SimpleDateFormat
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.FrameLayout
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import com.example.datvemaybay.R
import com.google.android.material.datepicker.CalendarConstraints
import com.google.android.material.datepicker.DateValidatorPointForward
import com.google.android.material.datepicker.MaterialDatePicker
import java.util.Date
import java.util.Locale

class DateFragment : Fragment() {

    private lateinit var departureDateText: TextView
    private lateinit var addReturnDateButton: Button
    private lateinit var calendarContainer: FrameLayout
    private lateinit var materialDatePicker: MaterialDatePicker<Long>
    private lateinit var returnDateContainer: LinearLayout
    private lateinit var returnDate: TextView

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_date, container, false)

        // Xử lý sự kiện của nút Cancel
        val returnButton = view.findViewById<ImageButton>(R.id.backButton)
        returnButton.setOnClickListener {
            requireActivity().supportFragmentManager.popBackStack()
        }

        departureDateText = view.findViewById<TextView>(R.id.departureDate)
        addReturnDateButton = view.findViewById<Button>(R.id.addReturnDate)
        calendarContainer = view.findViewById<FrameLayout>(R.id.calendarContainer)
        returnDateContainer = view.findViewById<LinearLayout>(R.id.returnDateContainer)
        returnDate = view.findViewById<TextView>(R.id.returnDate)

        // Hiển thị calendar khi fragment được tạo
        showNormalCalendar()

        // Xử lý sự kiện khi bấm vào nút "Add Return Date"
        addReturnDateButton.setOnClickListener {
            addReturnDateButton.visibility = View.GONE
            returnDateContainer.visibility = View.VISIBLE
            // Hiển thị DateRangePicker
            showDateRangePicker()
        }

        return view
    }

    // Hiển thị Calendar bình thường
    private fun showNormalCalendar() {
        val builder = MaterialDatePicker.Builder.datePicker()

        // Thiết lập các hạn chế lịch (nếu có)
        val constraintsBuilder = CalendarConstraints.Builder()
            .setValidator(DateValidatorPointForward.now()) // Chỉ cho phép chọn ngày từ hiện tại trở đi
        builder.setCalendarConstraints(constraintsBuilder.build())

        materialDatePicker = builder.build()

        // Xử lý khi người dùng chọn ngày
        materialDatePicker.addOnPositiveButtonClickListener { selection ->
            val sdf = SimpleDateFormat("dd/MMM/yyyy", Locale.getDefault())
            val selectedDate = sdf.format(Date(selection))

            // Hiển thị ngày đi
            departureDateText.text = selectedDate
        }

        // Hiển thị picker vào FrameLayout
        materialDatePicker.show(childFragmentManager, materialDatePicker.toString())
    }

    // Hiển thị DateRangePicker khi bấm vào nút "Add Return Date"
    private fun showDateRangePicker() {
        // Tạo bộ chọn ngày dạng range
        val builder = MaterialDatePicker.Builder.dateRangePicker()

        // Thiết lập các hạn chế lịch (nếu có)
        val constraintsBuilder = CalendarConstraints.Builder()
            .setValidator(DateValidatorPointForward.now()) // Chỉ cho phép chọn ngày từ hiện tại trở đi
        builder.setCalendarConstraints(constraintsBuilder.build())

        val dateRangePicker = builder.build()

        // Xử lý khi người dùng chọn ngày
        dateRangePicker.addOnPositiveButtonClickListener { selection ->
            val startDate = selection.first
            val endDate = selection.second

            // Chuyển đổi ngày từ Long thành Date để hiển thị
            val sdf = SimpleDateFormat("dd MMM yyyy", Locale.getDefault())
            val startDateString = sdf.format(Date(startDate))
            val endDateString = sdf.format(Date(endDate))

            // Hiển thị ngày đi và ngày về
            departureDateText.text = startDateString
            returnDate.text = endDateString
        }

        // Hiển thị picker vào FrameLayout
        dateRangePicker.show(childFragmentManager, dateRangePicker.toString())
    }
}