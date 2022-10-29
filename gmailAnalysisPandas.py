import imaplib
import email
from credentials import useName,passWord
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

imap_url ='imap.gmail.com'
my_mail = imaplib.IMAP4_SSL(imap_url)
my_mail.login(useName, passWord)

my_mail.select('Inbox')

data = my_mail.search(None, 'All')

mail_ids = data[1]  
id_list = mail_ids[0].split()   
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

email_df = pd.DataFrame(columns=['Date','From', 'Subject'], 
index=range(latest_email_id,first_email_id,-1))

for i in range(latest_email_id,first_email_id, -1):
    data = my_mail.fetch(str(i), '(RFC822)' )
    for response_part in data:
      arr = response_part[0]
      if isinstance(arr, tuple):
        msg = email.message_from_string(str(arr[1],'ISO-8859–1'))
        new_row = pd.Series({"Date":msg['Date'] , "From":msg['from']         , "Subject":msg['subject']})
    email_df = email_df.append(new_row, ignore_index=True)
    email_df['Date'] = pd.to_datetime(email_df['Date'])



email_df = email_df.dropna()
text = email_df['Subject'].values

stopwords = set(STOPWORDS)
stopwords.update([" "]) #You can add stopwords if you have any 
wordcloud = WordCloud(stopwords=stopwords, background_color="white", width=800, height=400).generate(str(text))
plt.figure(figsize = (15, 15), facecolor = None) 
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

email_df["plot_date"] = email_df["Date"].dt.strftime('%Y %m')
plt.style.use('dark_background')
plt.plot_date(email_df["plot_date"],email_df["From"], linestyle='solid')
plt.show()

