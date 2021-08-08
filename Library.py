from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
from datetime import datetime, timedelta
import tkinter.messagebox as message
import mysql.connector

username,userid=str(),str()

def loginpage():
    gameImg.pack_forget()
    loginbtn.pack_forget()
    frame1.pack(pady=30)
    msglbl.pack(pady=10)

def login():
    global username,userid
    entryid=identry.get()
    password=pwentry.get()
    query=f'SELECT name,pw FROM students WHERE id={entryid}'
    cursor.execute(query)
    result=cursor.fetchall()
    if result==[]:
        msg.set('No such user!Try again!!')
    else:
        dbusername,dbpw=result[0]
        if dbpw==password:
            username=dbusername
            userid=entryid
            homepage()
        else:
            msg.set('Wrong password!Try again!!')

def homepage():
    global username,userid
    frame1.pack_forget()
    msglbl.pack_forget()
    welcomelbl.config(text='Welcome '+username)
    query=f'SELECT * FROM students WHERE id={userid}'
    cursor.execute(query)
    result=cursor.fetchall()
    studentid.set('Roll number: '+str(result[0][0]))
    studentdept.set('Department: '+result[0][3])
    studentyear.set('Year of study: '+str(result[0][2]))
    frame2.pack(pady=30)
    
def explorepage():
    welcomelbl.pack_forget()
    frame2.pack_forget()
    frame4.pack(fill=X)
    frame5.pack(pady=10)

def issuespage():
    global userid
    sid=userid
    welcomelbl.pack_forget()
    frame2.pack_forget()
    frame4.pack(fill=X)
    query=f'SELECT bookid,book,issuedate,returndate FROM issues WHERE sid={sid}'
    cursor.execute(query)
    result=cursor.fetchall()
    issuesframe.columnconfigure(0,minsize=10)
    issuesframe.columnconfigure(1,minsize=300)
    issuesframe.columnconfigure(2,minsize=100)
    issuesframe.columnconfigure(3,minsize=100)
    labels=['ID','BOOK-NAME','ISSUE-DATE','RETURN-DATE']
    col=0
    for x in labels:
        Label(issuesframe,text=x,fg='orange',bg='black').grid(row=0,column=col)
        col+=1
    if result==[]:
        pass
    else:
        i,j=1,0
        for book in result:
            for attr in book:
                Label(issuesframe,text=str(attr),fg='white',bg='black').grid(row=i,column=j,pady=2)
                j+=1
            i+=1
            j=0
        issuesframe.pack(pady=10)

def bookissuepage():
    welcomelbl.pack_forget()
    frame2.pack_forget()
    frame4.pack(fill=X)
    frame6.pack(pady=50)

def bookissue():
    global userid
    bookid=bookentry.get()
    query1=f'SELECT * FROM books WHERE bookid={bookid}'
    cursor.execute(query1)
    result=cursor.fetchall()
    if result==[]:
        message.showinfo("Error","Book not found!!")
    else:
        query2="INSERT INTO issues (sid,bookid,book,issuedate,returndate) VALUES (%s,%s,%s,%s,%s)"
        sid=userid
        book=result[0][1]
        today=datetime.now()
        issuedate=today.strftime('%d/%m/%Y')
        ret=today+timedelta(15)
        returndate=ret.strftime('%d/%m/%Y')
        values=(sid,bookid,book,issuedate,returndate)
        try:
            cursor.execute(query2,values)
            conn.commit()
            message.showinfo("Result",f"Book-ID {bookid} issued")
        except:
            conn.rollback()
            message.showinfo("Result","Not able to issue book!Try again!")

def returnbookpage():
    welcomelbl.pack_forget()
    frame2.pack_forget()
    frame4.pack(fill=X)
    returnframe.pack(pady=50)

def returnbook():
    global userid
    bookid=bookentry2.get()
    query1=f'SELECT * FROM issues WHERE sid={userid} AND bookid={bookid}'
    cursor.execute(query1)
    result=cursor.fetchall()
    if result==[]:
        message.showinfo("Error","Book not found!!")
    else:
        query2=f'DELETE FROM issues WHERE sid={userid} AND bookid={bookid}'
        try:
            cursor.execute(query2)
            conn.commit()
            message.showinfo("Result",f"Book-ID {bookid} returned")
        except:
            conn.rollback()
            message.showinfo("Result","Not able to return book!Try again!")

def returnhome():
    frame4.pack_forget()
    frame5.pack_forget()
    frame6.pack_forget()
    returnframe.pack_forget()
    for widgets in booksframe.winfo_children():
        widgets.destroy()
    booksframe.pack_forget()
    for widgets in issuesframe.winfo_children():
        widgets.destroy()
    issuesframe.pack_forget()
    welcomelbl.pack()
    homepage()

def displaybooks(secid):
    frame5.pack_forget()
    query=f'select bookid,book_name,author,edition,publisher from books where secid={secid}'
    cursor.execute(query)
    result=cursor.fetchall()
    booksframe.columnconfigure(0,minsize=10)
    booksframe.columnconfigure(1,minsize=300)
    booksframe.columnconfigure(2,minsize=200)
    booksframe.columnconfigure(3,minsize=10)
    booksframe.columnconfigure(4,minsize=200)
    labels=['ID','NAME','AUTHOR','EDITION','PUBLISHER']
    col=0
    for x in labels:
        Label(booksframe,text=x,fg='orange',bg='black').grid(row=0,column=col)
        col+=1
    i,j=1,0
    for book in result:
        for attr in book:
            Label(booksframe,text=str(attr),fg='white',bg='black').grid(row=i,column=j,pady=2)
            j+=1
        i+=1
        j=0
    booksframe.pack(pady=10)

if __name__=="__main__":
    #Establishing the connection
    conn=mysql.connector.connect(host='localhost',database='library',user='root',password='pw123')
    cursor=conn.cursor()
    
    #creating the root window
    root = Tk()
    root.title('Library App')
    root.geometry('800x600')
    root.iconbitmap(r'libicon.ico')
    root.resizable(False,False)
    welcomelbl=Label(root,text='Welcome to Library App',width=30,font=("Arial bold",20),bg='black',fg='white')
    welcomelbl.pack()
    img = ImageTk.PhotoImage(Image.open("pic2.jpg"))
    gameImg = Label(root,image=img)
    gameImg.pack(pady=30)
    loginbtn = Button(root,text="Login",fg="red",bg="black",pady=10,padx=20,command=loginpage)
    myFont = font.Font(family='Courier', size=20, weight='bold')
    loginbtn['font']=myFont
    loginbtn.pack()
    
    #login page widgets
    frame1=Frame(root,width=400,height=300,highlightbackground="green", highlightcolor="green", highlightthickness=3)
    idlbl=Label(frame1,text='Roll number')
    identry=Entry(frame1,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    pwlbl=Label(frame1,text='Password')
    pwentry=Entry(frame1,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    submitbtn=Button(frame1,text='submit',padx=5,pady=5,fg='red',command=login)
    idlbl.place(x = 50, y = 100)
    identry.place(x = 150, y = 100, width = 200)
    pwlbl.place(x = 50, y = 150)
    pwentry.place(x = 150, y = 150, width = 200)
    submitbtn.place(x=220,y=200)
    msg=StringVar()
    msglbl=Label(root,font=('Times 15 bold'),textvariable=msg)
    
    #home page widgets
    frame2=Frame(root)
    frame3=Frame(frame2,width=400,height=300,highlightbackground="green", highlightcolor="green", highlightthickness=3)
    frame3.pack()
    studentid=StringVar()
    studentid_lbl=Label(frame3,font=('Times 15 bold'),textvariable=studentid)
    studentid_lbl.pack(pady=7)
    studentdept=StringVar()
    studentdept_lbl=Label(frame3,font=('Times 15 bold'),textvariable=studentdept)
    studentdept_lbl.pack(pady=7)
    studentyear=StringVar()
    studentyear_lbl=Label(frame3,font=('Times 15 bold'),textvariable=studentyear)
    studentyear_lbl.pack(pady=7)
    explorebtn = Button(frame2,text="Explore books",fg="red",bg="black",pady=10,padx=15,command=explorepage)
    myFont = font.Font(family='Courier', size=10, weight='bold')
    explorebtn['font']=myFont
    explorebtn.pack(pady=15)
    viewbtn = Button(frame2,text="Book issues",fg="red",bg="black",pady=10,padx=15,command=issuespage)
    viewbtn['font']=myFont
    viewbtn.pack(pady=15)
    issuebtn = Button(frame2,text="Issue book",fg="red",bg="black",pady=10,padx=15,command=bookissuepage)
    issuebtn['font']=myFont
    issuebtn.pack(pady=15)
    returnbtn = Button(frame2,text="Return book",fg="red",bg="black",pady=10,padx=15,command=returnbookpage)
    returnbtn['font']=myFont
    returnbtn.pack(pady=15)

    #explore page widgets
    frame4=Frame(root,highlightbackground="red", highlightcolor="red", highlightthickness=1)
    photo1 = PhotoImage(file = r"back.png")
    photoimage1 = photo1.subsample(10, 10)
    backbtn=Button(frame4, text = 'home', image = photoimage1,compound = LEFT,padx=10,fg='blue',command=returnhome)
    backbtn.grid(row=0,column=0,sticky=W)
    frame5=Frame(root)
    csitbtn = Button(frame5,text="CS/IT",fg="yellow",bg="black",pady=10,padx=15,command=lambda:displaybooks(1))
    ecebtn = Button(frame5,text="ECE",fg="yellow",bg="black",pady=10,padx=15,command=lambda:displaybooks(2))
    eeebtn = Button(frame5,text="EEE",fg="yellow",bg="black",pady=10,padx=15,command=lambda:displaybooks(3))
    mecbtn = Button(frame5,text="MEC",fg="yellow",bg="black",pady=10,padx=15,command=lambda:displaybooks(4))
    myFont = font.Font(family='Courier', size=15, weight='bold')
    csitbtn['font']=myFont
    ecebtn['font']=myFont
    eeebtn['font']=myFont
    mecbtn['font']=myFont
    csitbtn.pack(pady=20)
    ecebtn.pack(pady=20)
    eeebtn.pack(pady=20)
    mecbtn.pack(pady=20)

    #displaybooks page widgets
    booksframe=Frame(root,bg='black')
    
    #bookissue-page widgets
    frame6=Frame(root,width=400,height=200,highlightbackground="green", highlightcolor="green", highlightthickness=3)
    booklbl=Label(frame6,text='Enter book id',font=('Times 15 bold'))
    bookentry=Entry(frame6,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    booklbl.place(x = 50, y = 100)
    bookentry.place(x = 200, y = 100, width = 150)
    booksubmitbtn=Button(frame6,text='submit',padx=5,pady=5,fg='red',command=bookissue)
    booksubmitbtn.place(x=250,y=150)

    #issuespage widgets
    issuesframe=Frame(root,bg='black')

    #returnpage widgets
    returnframe=Frame(root,width=400,height=200,highlightbackground="green", highlightcolor="green", highlightthickness=3)
    booklbl2=Label(returnframe,text='Enter book id',font=('Times 15 bold'))
    bookentry2=Entry(returnframe,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    booklbl2.place(x = 50, y = 100)
    bookentry2.place(x = 200, y = 100, width = 150)
    booksubmitbtn2=Button(returnframe,text='submit',padx=5,pady=5,fg='red',command=returnbook)
    booksubmitbtn2.place(x=250,y=150)
    
    root.mainloop()
