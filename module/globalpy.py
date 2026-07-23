
class GlobalVar():
    json_data = {
        # The schedule template message sent by bot
        "schedule" : "",

        # 'ryuh check' will trigger bot to send result message, this saves the result message
        "schedule_check_result": "",

        # 0 - not done for the month
        # 1 - done for the month
        # Default to not done
        "black_mage_done": "0",
        # tell me which month done/not done
        # default to "Current Month"
        "black_mage_month": "Current Month",
    }
