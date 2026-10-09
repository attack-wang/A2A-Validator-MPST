    legend_x = min(width - 10, cx + r + 16)
    legend_y = 40
    for (label, value), color in zip(data.items(), colors):
        percentage = 100.0 * value / total
        canvas.create_rectangle(legend_x, legend_y, legend_x + 12, legend_y + 12,
                                fill=color, outline="")
        canvas.create_text(legend_x + 18, legend_y + 6, anchor="w",
                           text=f"{label} ({percentage:.1f}%)",
                           font=("Helvetica", 9), fill=TEXT_COLOR)
        legend_y += 18