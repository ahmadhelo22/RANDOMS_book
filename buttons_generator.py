
def button_generater_func(new_sentences, the_text, links, InlineKeyboardButton,InlineKeyboardMarkup, msg):

    try:
            

        num_of_rows = len(new_sentences)
        num_of_buttons = 1

        if the_text == None:
            text = 'اختر الكتاب'
        else :
            text = the_text

        buttons = []

        for i in range(num_of_rows):
            row = []
            for j in range(num_of_buttons):
                button_text = new_sentences[i]
                button_callback = links[i]  # قم بتعديل هنا لاستخدام الروابط
                row.append(InlineKeyboardButton(button_text, url=button_callback))  # استخدم `url` بدلاً من `callback_data`
            buttons.append(row)

        keyboard = InlineKeyboardMarkup(buttons)
        a = msg.reply_text(text, reply_markup=keyboard)
        return a

    except:
        
        return  msg.reply_text ('يوجد مشكله باظهار النتائج جرب ')
