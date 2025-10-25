# main_android.py
# -*- coding: utf-8 -*-
import os
import random
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# Android兼容性设置
from kivy.utils import platform
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET])
    
    # 使用Android数据目录
    from android.storage import app_storage_path
    from android import mActivity
    data_dir = app_storage_path()
else:
    data_dir = os.getcwd()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.text import LabelBase

# 中文字体处理
try:
    if platform == 'android':
        # Android使用默认字体
        CHINESE_FONT = 'DroidSansFallback'
    else:
        # Windows尝试微软雅黑
        LabelBase.register(name='MicrosoftYaHei', fn_regular='C:/Windows/Fonts/msyh.ttc')
        CHINESE_FONT = 'MicrosoftYaHei'
    print("字体设置完成")
except:
    CHINESE_FONT = None
    print("使用默认字体")

class ElectricityReminderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化用户数据
        self.user_data = {
            "dormitory": "A101",
            "remaining_electricity": 25.0,
            "daily_usage": 2.5,
            "phone": "13800138000"
        }
        self.warning_levels = {
            "normal": 20,    # 一般提醒
            "urgent": 10,    # 紧急提醒
            "critical": 5    # 强提示
        }
        
    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title_label = Label(
            text='容大后勤电费提醒',
            size_hint_y=None,
            height=50,
            font_size=24,
            bold=True,
            font_name=CHINESE_FONT
        )
        main_layout.add_widget(title_label)
        
        # 创建可滚动的内容区域
        scroll_view = ScrollView()
        content_layout = BoxLayout(
            orientation='vertical', 
            spacing=15,
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # 当前电量状态卡片
        status_card = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=200
        )
        
        status_title = Label(
            text='当前电量状态',
            size_hint_y=None,
            height=30,
            font_size=18,
            bold=True,
            font_name=CHINESE_FONT
        )
        status_card.add_widget(status_title)
        
        self.remaining_label = Label(
            text=f'{self.user_data["remaining_electricity"]} 度',
            font_size=32,
            size_hint_y=None,
            height=50,
            font_name=CHINESE_FONT
        )
        status_card.add_widget(self.remaining_label)
        
        # 进度条
        self.progress_bar = ProgressBar(
            max=100,
            value=self.user_data["remaining_electricity"],
            size_hint_y=None,
            height=20
        )
        status_card.add_widget(self.progress_bar)
        
        # 预计剩余天数
        days_label = Label(
            text='预计还可使用:',
            size_hint_y=None,
            height=30,
            font_size=16,
            font_name=CHINESE_FONT
        )
        status_card.add_widget(days_label)
        
        self.days_value = Label(
            text=f'{self.user_data["remaining_electricity"]/self.user_data["daily_usage"]:.1f} 天',
            font_size=20,
            size_hint_y=None,
            height=40,
            font_name=CHINESE_FONT
        )
        status_card.add_widget(self.days_value)
        
        content_layout.add_widget(status_card)
        
        # 预警级别卡片
        warning_card = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=120
        )
        
        warning_title = Label(
            text='预警设置',
            size_hint_y=None,
            height=30,
            font_size=18,
            bold=True,
            font_name=CHINESE_FONT
        )
        warning_card.add_widget(warning_title)
        
        warning_info = Label(
            text=f'一般提醒: 低于 {self.warning_levels["normal"]} 度\n'
                 f'紧急提醒: 低于 {self.warning_levels["urgent"]} 度\n'
                 f'强提示: 低于 {self.warning_levels["critical"]} 度',
            size_hint_y=None,
            height=80,
            font_size=14,
            font_name=CHINESE_FONT
        )
        warning_card.add_widget(warning_info)
        
        content_layout.add_widget(warning_card)
        
        # 快捷操作卡片
        actions_card = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=120
        )
        
        actions_title = Label(
            text='快捷操作',
            size_hint_y=None,
            height=30,
            font_size=18,
            bold=True,
            font_name=CHINESE_FONT
        )
        actions_card.add_widget(actions_title)
        
        # 按钮布局
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50
        )
        
        recharge_btn = Button(
            text='立即充值',
            on_press=self.recharge_electricity,
            font_name=CHINESE_FONT
        )
        buttons_layout.add_widget(recharge_btn)
        
        check_btn = Button(
            text='手动检查',
            on_press=self.manual_check,
            font_name=CHINESE_FONT
        )
        buttons_layout.add_widget(check_btn)
        
        actions_card.add_widget(buttons_layout)
        content_layout.add_widget(actions_card)
        
        # 用电建议卡片
        tips_card = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height=180
        )
        
        tips_title = Label(
            text='用电常识与建议',
            size_hint_y=None,
            height=30,
            font_size=18,
            bold=True,
            font_name=CHINESE_FONT
        )
        tips_card.add_widget(tips_title)
        
        tips_content = Label(
            text='• 合理使用空调，温度设置在26℃为宜\n'
                 '• 离开宿舍时关闭不必要的电器\n'
                 '• 使用节能灯具和设备\n'
                 '• 定期检查电器设备运行状态',
            size_hint_y=None,
            height=140,
            font_size=14,
            font_name=CHINESE_FONT
        )
        tips_card.add_widget(tips_content)
        
        content_layout.add_widget(tips_card)
        
        # 将内容添加到滚动视图
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        # 开始电量监控
        Clock.schedule_interval(self.check_electricity, 10)
        
        return main_layout
    
    def check_electricity(self, dt=None):
        """检查电量并触发相应提醒"""
        # 模拟电量消耗
        self.user_data["remaining_electricity"] = max(
            0, 
            self.user_data["remaining_electricity"] - 1.2*random.random()
        )
        
        # 更新显示
        self.update_display()
        
        # 检查预警条件
        remaining = self.user_data["remaining_electricity"]
        
        if remaining <= self.warning_levels["critical"] and remaining > 0:
            self.show_critical_warning()
        elif remaining <= self.warning_levels["urgent"]:
            self.show_urgent_warning()
        elif remaining <= self.warning_levels["normal"]:
            self.show_normal_warning()
    
    def update_display(self):
        """更新显示当前电量数据"""
        remaining = self.user_data["remaining_electricity"]
        daily_usage = self.user_data["daily_usage"]
        
        # 计算预计剩余天数
        days_remaining = remaining / daily_usage if daily_usage > 0 else 0
        
        # 更新标签
        self.remaining_label.text = f'{remaining:.1f} 度'
        self.days_value.text = f'{days_remaining:.1f} 天'
        
        # 更新进度条
        self.progress_bar.value = remaining
    
    def show_normal_warning(self):
        """一般提醒（低于20度）"""
        self.show_warning_popup(
            "电量提醒",
            f"您的宿舍{self.user_data['dormitory']}剩余电量{self.user_data['remaining_electricity']:.1f}度。"
            f"预计还可使用{self.user_data['remaining_electricity']/self.user_data['daily_usage']:.1f}天。"
            "建议及时充值，避免影响使用。",
            "normal"
        )
    
    def show_urgent_warning(self):
        """紧急提醒（低于10度）"""
        self.show_warning_popup(
            "紧急电量提醒",
            f"您的宿舍{self.user_data['dormitory']}剩余电量仅{self.user_data['remaining_electricity']:.1f}度！"
            "请立即充值，否则很快将断电。",
            "urgent"
        )
    
    def show_critical_warning(self):
        """强提示（低于5度）"""
        self.show_warning_popup(
            "电量严重不足！",
            f"警告！您的宿舍{self.user_data['dormitory']}即将断电！"
            f"剩余电量仅{self.user_data['remaining_electricity']:.1f}度！"
            "请立即充值！",
            "critical"
        )
    
    def show_warning_popup(self, title, message, level):
        """显示预警弹窗"""
        # 创建弹窗内容
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 消息标签
        message_label = Label(
            text=message,
            text_size=(300, None),
            font_name=CHINESE_FONT
        )
        popup_content.add_widget(message_label)
        
        # 按钮布局
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        # 充值按钮
        recharge_btn = Button(
            text='立即充值',
            on_press=lambda instance: self.recharge_electricity(instance),
            font_name=CHINESE_FONT
        )
        buttons_layout.add_widget(recharge_btn)
        
        # 稍后提醒按钮
        later_btn = Button(
            text='稍后提醒',
            on_press=lambda instance: self.popup.dismiss(),
            font_name=CHINESE_FONT
        )
        buttons_layout.add_widget(later_btn)
        
        popup_content.add_widget(buttons_layout)
        
        # 创建并打开弹窗
        self.popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        self.popup.open()
    
    def recharge_electricity(self, instance=None):
        """模拟充值操作"""
        # 增加30度电模拟充值
        self.user_data["remaining_electricity"] += 30
        self.update_display()
        
        # 如果是从弹窗调用的，关闭弹窗
        if hasattr(self, 'popup'):
            self.popup.dismiss()
        
        # 显示确认信息
        self.show_confirmation_popup("充值成功！已增加30度电。")
    
    def show_confirmation_popup(self, message):
        """显示确认弹窗"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        message_label = Label(
            text=message,
            font_name=CHINESE_FONT
        )
        content.add_widget(message_label)
        
        ok_btn = Button(
            text='确定',
            size_hint_y=None,
            height=40,
            on_press=lambda instance: self.confirmation_popup.dismiss(),
            font_name=CHINESE_FONT
        )
        content.add_widget(ok_btn)
        
        self.confirmation_popup = Popup(
            title='成功',
            content=content,
            size_hint=(0.6, 0.4)
        )
        self.confirmation_popup.open()
    
    def manual_check(self, instance=None):
        """手动检查电量"""
        self.check_electricity()

if __name__ == '__main__':
    ElectricityReminderApp().run()
