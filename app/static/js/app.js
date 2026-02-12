/**
 * 月升月落应用的Alpine.js逻辑
 */

function moonApp() {
    return {
        // 状态数据
        selectedCity: 'beijing',
        selectedYear: new Date().getFullYear(),
        selectedMonth: new Date().getMonth() + 1,
        monthData: null,
        selectedDayData: null,
        loading: false,
        error: null,
        startDayOfWeek: 0,

        /**
         * 初始化函数
         */
        init() {
            this.loadMonthData();
        },

        /**
         * 加载整月数据
         */
        async loadMonthData() {
            this.loading = true;
            this.error = null;
            this.selectedDayData = null;

            try {
                const url = `/api/calendar/${this.selectedCity}/${this.selectedYear}/${this.selectedMonth}`;
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error('加载数据失败');
                }

                this.monthData = await response.json();

                // 计算该月第一天是星期几（用于日历网格对齐）
                const firstDay = new Date(this.selectedYear, this.selectedMonth - 1, 1);
                this.startDayOfWeek = firstDay.getDay();

                // 默认选中当前日期（如果在当前月）
                const today = new Date();
                if (this.selectedYear === today.getFullYear() &&
                    this.selectedMonth === today.getMonth() + 1) {
                    const todayData = this.monthData.days.find(d => d.day === today.getDate());
                    if (todayData) {
                        this.selectedDayData = todayData;
                    }
                }

            } catch (err) {
                this.error = '加载月相数据失败：' + err.message;
                console.error(err);
            } finally {
                this.loading = false;
            }
        },

        /**
         * 上一个月
         */
        previousMonth() {
            if (this.selectedMonth === 1) {
                this.selectedMonth = 12;
                this.selectedYear--;
            } else {
                this.selectedMonth--;
            }
            this.loadMonthData();
        },

        /**
         * 下一个月
         */
        nextMonth() {
            if (this.selectedMonth === 12) {
                this.selectedMonth = 1;
                this.selectedYear++;
            } else {
                this.selectedMonth++;
            }
            this.loadMonthData();
        },

        /**
         * 选中某一天
         */
        selectDay(dayData) {
            this.selectedDayData = dayData;
        }
    };
}
