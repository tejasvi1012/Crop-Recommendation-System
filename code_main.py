from tkinter import*
#import mysql.connector
from PIL import Image,ImageTk
import webbrowser
import joblib
import google.generativeai as genai
#import smtplib
top=Tk()
top.geometry("1500x1000")
top.title("AGRIWISE")

i0=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\welcome.png")
p0=ImageTk.PhotoImage(i0)

l=Label(top,image=p0)
l.place(x=0,y=0)

global soil
soil=IntVar()
water=IntVar()
season=IntVar()
global s
global z
global x
global y
z=0
x=0
y=0

#home page_____________________________________________________________________________________________________________________________



l=Label(top,text="AGRO INDIA",font="helvetica 30 bold",bg="lightblue",padx=600).place(x=20,y=40)

i=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\happy_farmer.jpg")
p=ImageTk.PhotoImage(i)

l=Label(top,image=p)
l.place(x=100,y=110)

ii=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\logo.jpg")
pp=ImageTk.PhotoImage(ii)

l=Label(top,image=pp)
l.place(x=570,y=110)

ii1=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\drone.jpg")
pp1=ImageTk.PhotoImage(ii1)

l=Label(top,image=pp1)
l.place(x=900,y=110)

l=Label(top,text="Welcome to our cutting-edge agricultural software solution!\n Our mission is to empower farmers with advanced technology to optimize crop yields, reduce resource wastage, and enhance overall productivity.\n Explore our intuitive tools, real-time data analytics, and expert recommendations to revolutionize your farming practices and cultivate a sustainable future.",font="arial 12 bold")
l.place(x=140,y=400)

l=Label(top,text="SELECT THE FIELD:",font="helvetica 15 bold")
l.place(x=680,y=520)


#crop suggestion section______________________________________________________________________________________________________________________


# Load ML model
model = joblib.load("crop_recommendation_model.pkl")

# Soil and water level mappings
soil_npk_map = {
    "Red Soil": [60, 30, 35],
    "Black Soil": [70, 50, 40],
    "Alluvial Soil": [90, 42, 43],
    "Clayey Soil": [65, 40, 38]
}

water_rainfall_map = {
    "High": 250,
    "Medium": 150,
    "Low": 50
}

def crop():
    top = Toplevel()
    top.geometry("1500x1000")
    top.title("Crop Suggestion")

    Label(top, text="Select Soil Type:", font=("Arial", 14)).pack(pady=10)
    soil_var = StringVar()
    soil_var.set("")  # Uncheck all soil options initially
    selected_npk = []

    soil_images = {
        "Red Soil": "C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/redsoil.jpg",
        "Black Soil": "C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/blacksoil.jpg",
        "Alluvial Soil": "C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/aluvialsoil.jpg",
        "Clayey Soil": "C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/claveysoil.jpg"
    }

    soil_frame = Frame(top)
    soil_frame.pack(pady=5)
    soil_var.set("")

    for soil, img_path in soil_images.items():
        frame = Frame(soil_frame)
        frame.pack(side=LEFT, padx=10)

        img = Image.open(img_path).resize((150, 150))
        photo = ImageTk.PhotoImage(img)
        lbl = Label(frame, image=photo)
        lbl.image = photo
        lbl.pack()

        radio = Radiobutton(
            frame,
            text=soil,
            variable=soil_var,
            value=soil,
            command=lambda s=soil: selected_npk.clear() or selected_npk.extend(soil_npk_map[s]),
            font=("Arial", 12),
            indicatoron=0,  # You can change to 0 if you want button-style
            padx=5,
            pady=5
        )
        radio.pack()


    Label(top, text="Select Water Availability:", font=("Arial", 14)).pack(pady=10)
    water_var = StringVar()
    water_var.set("")  # Uncheck all water options initially
    selected_rain = []
    water_images = {
        "High": "C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/high.png",
        "Medium": "C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/medium.png",
        "Low": "C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/low.png"
    }

    water_frame = Frame(top)
    water_frame.pack(pady=5)
    for level, img_path in water_images.items():
        frame = Frame(water_frame)
        frame.pack(side=LEFT, padx=10)

        img = Image.open(img_path).resize((150, 100))
        photo = ImageTk.PhotoImage(img)
        lbl = Label(frame, image=photo)
        lbl.image = photo
        lbl.pack()

        radio = Radiobutton(
            frame,
            text=level,
            variable=water_var,
            value=level,
            command=lambda l=level: selected_rain.clear() or selected_rain.append(water_rainfall_map[l]),
            font=("Arial", 12),        # Bigger font
            indicatoron=0,             # Shows standard radio buttons
            padx=5,
            pady=5
        )
        radio.pack()


    Label(top, text="Enter Temperature (°C) [8 - 43]:", font=("Arial", 12)).pack(pady=5)
    temp_entry = Entry(top)
    temp_entry.pack(pady=5)

    Label(top, text="Enter Humidity (%) [14 - 100]:", font=("Arial", 12)).pack(pady=5)
    hum_entry = Entry(top)
    hum_entry.pack(pady=5)

    Label(top, text="Enter pH [0 - 14]:", font=("Arial", 12)).pack(pady=5)
    ph_entry = Entry(top)
    ph_entry.pack(pady=5)
    # Valid ranges from the dataset
    TEMP_MIN = 8.82
    TEMP_MAX = 43.68
    HUM_MIN = 14.26
    HUM_MAX = 99.98


    def open_prediction():
        try:
            temp = float(temp_entry.get())
            hum = float(hum_entry.get())
            ph = float(ph_entry.get())

# Check if temperature and humidity are within valid range
            if not (TEMP_MIN <= temp <= TEMP_MAX):
                raise ValueError("Temperature out of range.")
            if not (HUM_MIN <= hum <= HUM_MAX):
                raise ValueError("Humidity out of range.")


            npk = selected_npk
            rainfall = selected_rain[0] if selected_rain else 0

            sample = [[npk[0], npk[1], npk[2], temp, hum, ph, rainfall]]
            prediction = model.predict(sample)[0]

            result_window = Toplevel()
            result_window.geometry("1500x1000")
            result_window.title("Prediction Result")
            Label(result_window, text=f"Recommended Crop: {prediction.upper()}", font=("Arial", 20, "bold"), fg="green").pack(pady=80)

        except ValueError:
            result_window = Toplevel()
            result_window.geometry("400x200")
            result_window.title("Error")
            Label(result_window, text="Please enter valid numeric values.", font=("Arial", 14), fg="red").pack(pady=40)

    Button(top, text="Suggest Crop", command=open_prediction, font=("Arial", 14), bg="lightgreen").pack(pady=20)
    top.mainloop()
#chatbot_____


# ===== CONFIGURE API KEY =====
genai.configure(api_key="AIzaSyAIqNAIrnDa-KFqH2Gd6dfp-aYOQ0d5fg8")

# ===== GUI APP FUNCTION =====
def chatbot():
    top = Toplevel()
    top.geometry("600x700")
    top.title("Agro India Chatbot - Gemini")

    Label(top, text="Ask your farming-related questions!", font=("Arial", 16, "bold"), bg="lightgreen", pady=10).pack(fill=X)

    text_area = Text(top, wrap=WORD, font=("Arial", 12))
    text_area.pack(padx=10, pady=10, expand=True, fill=BOTH)

    entry = Entry(top, font=("Arial", 14))
    entry.pack(padx=10, pady=5, fill=X)

    # Initialize a **chat session**
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Using a generally available model

    def ask_gemini():
        question = entry.get()
        if not question.strip():
            return
        text_area.insert(END, f"You: {question}\n")

        try:
            response = model.generate_content(question)
            answer = response.text.strip()
            text_area.insert(END, f"AgroBot: {answer}\n\n")
        except Exception as e:
            text_area.insert(END, f"Error: {str(e)}\n\n")

        entry.delete(0, END)

    Button(top, text="Ask", font=("Arial", 14), bg="lightblue", command=ask_gemini).pack(pady=5)

    top.mainloop()





#______
#fertilizers suggestion section__________________________________________________________________________________________________



def fertilizer():
    top4=Toplevel()
    top4.geometry("1500x1000")
    
    top4.title("AGRO INDIA")
    l=Label(top4,text="          FERTILIZERS                ",font="arial 25 bold",fg="black",bg="lightblue",padx=500).place(x=10,y=20)
    l=Label(top4,text="SELECT THE CROP:",font="arial 16 bold",fg="black").place(x=50,y=90)
    l=Label(top4,text="FERTILIZER:",font="arial 16 bold",fg="black").place(x=50,y=400)
    l=Label(top4,text="FERTILIZER DETAILS:",font="arial 16 bold",fg="black").place(x=850,y=400)


    def paddyfertilizer():

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=230,y=450)

        i35=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p35=ImageTk.PhotoImage(i35)

        l=Label(top4,image=p35)
        l.place(x=830,y=450)

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\paddy_fertilizer_det.jpg")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=830,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\paddy_fertilizer.jpg")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()


    def maizefertilizer():
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=230,y=450)

        i35=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p35=ImageTk.PhotoImage(i35)

        l=Label(top4,image=p35)
        l.place(x=830,y=450)


        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\maize_fertilizer_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=830,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\maize_fertilizer.png")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def groundnutfertilizer():
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=230,y=450)

        i35=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p35=ImageTk.PhotoImage(i35)

        l=Label(top4,image=p35)
        l.place(x=830,y=450)

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\groundnut_fertilizer_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=830,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\groundnut_fertilizer.png")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def cottonfertilizer():

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=230,y=450)

        i35=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p35=ImageTk.PhotoImage(i35)

        l=Label(top4,image=p35)
        l.place(x=830,y=450)
        
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\cotton_fetilizer_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=830,y=450)
        
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\cotton_fertilizer.png")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def sunflowerfertilizer():
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=230,y=450)

        i35=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p35=ImageTk.PhotoImage(i35)

        l=Label(top4,image=p35)
        l.place(x=830,y=450)

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\sunflower_fertilizer_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=830,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\sunflower_fertilizer.png")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def wheatfertilizer():
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=230,y=450)

        i35=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg.jpg")
        p35=ImageTk.PhotoImage(i35)

        l=Label(top4,image=p35)
        l.place(x=830,y=450)

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\wheat_fertilizer_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=830,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\wheat_fertilizer.png")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()
    
    
    i27=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\paddy.jpg")
    p27=ImageTk.PhotoImage(i27)
    b=Button(top4,image=p27,command=paddyfertilizer)
    b.place(x=50,y=150)
    
    
    i28=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\maize.jpg")
    p28=ImageTk.PhotoImage(i28)
    b=Button(top4,image=p28,command=maizefertilizer)
    b.place(x=300,y=160)
    
    
    i29=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\groundnut.jpg")
    p29=ImageTk.PhotoImage(i29)
    b=Button(top4,image=p29,command=groundnutfertilizer)
    b.place(x=550,y=150)
    
    
    i30=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\cotton.jpg")
    p30=ImageTk.PhotoImage(i30)
    b=Button(top4,image=p30,command=cottonfertilizer)
    b.place(x=800,y=150)

    i31=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\sunflower.jpg")
    p31=ImageTk.PhotoImage(i31)
    b=Button(top4,image=p31,command=sunflowerfertilizer)
    b.place(x=1050,y=150)

    i32=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\wheat.jpg")
    p32=ImageTk.PhotoImage(i32)
    b=Button(top4,image=p32,command=wheatfertilizer)
    b.place(x=1300,y=150)
    
    l=Label(top4,text="PADDY",font="arial 12 bold").place(x=120,y=290)
    l=Label(top4,text="MAIZE",font="arial 12 bold").place(x=370,y=290)
    
    l=Label(top4,text="GROUNDNUT",font="arial 12 bold").place(x=600,y=290)
    l=Label(top4,text="COTTON",font="arial 12 bold").place(x=850,y=290)
    l=Label(top4,text="SUNFLOWER",font="arial 12 bold").place(x=1100,y=290)
    l=Label(top4,text="WHEAT",font="arial 12 bold").place(x=1350,y=290)

    top4.mainloop()

    #pesticide
def pesticide():
    
    top4=Toplevel()
    top4.geometry("1500x1000")
    
    top4.title("AGRO INDIA")
    l=Label(top4,text="          PESTICIDES                ",font="arial 25 bold",fg="black",bg="lightblue",padx=500).place(x=10,y=20)
    l=Label(top4,text="SELECT THE CROP:",font="arial 16 bold",fg="black").place(x=50,y=90)
    l=Label(top4,text="MAJOR PESTS:",font="arial 16 bold",fg="black").place(x=50,y=400)
    l=Label(top4,text="PESTICIDE DETAILS:",font="arial 16 bold",fg="black").place(x=550,y=400)


    def paddypesticide():

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebgpest.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=10,y=450)

        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\paddy_pesticide.png")
        p36=ImageTk.PhotoImage(i36)

        l=Label(top4,image=p36)
        l.place(x=600,y=450)

        i37=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\paddy_pesticide_det.png")
        p37=ImageTk.PhotoImage(i37)

        l=Label(top4,image=p37)
        l.place(x=880,y=480)
        
        i38=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\Paddy_insect.png")
        p38=ImageTk.PhotoImage(i38)

        l=Label(top4,image=p38)
        l.place(x=130,y=450)
        
        top4.mainloop()


    def maizepesticide():
        
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebgpest.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=10,y=450)

        i37=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\maize_pesticide_det.png")
        p37=ImageTk.PhotoImage(i37)

        l=Label(top4,image=p37)
        l.place(x=900,y=450)
        


        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\maize_pesticide.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=600,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\maize_pest.jpg")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def groundnutpesticide():
        
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebgpest.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=10,y=450)


        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\groundnut_pesticide.png")
        p36=ImageTk.PhotoImage(i36)

        l=Label(top4,image=p36)
        l.place(x=600,y=450)

        

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\groundnut_pesticide_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=890,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\groundnut_pest.jpg")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def cottonpesticide():

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebgpest.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=10,y=450)

        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\cotton_pesticide.png")
        p36=ImageTk.PhotoImage(i36)

        l=Label(top4,image=p36)
        l.place(x=600,y=450)
        
        
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\cotton_pesticide_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=890,y=450)
        
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\cotton_pest.jpg")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def sunflowerpesticide():
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebgpest.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=10,y=450)
        

        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\sunflower_pesticide.png")
        p36=ImageTk.PhotoImage(i36)

        l=Label(top4,image=p36)
        l.place(x=600,y=450)
        

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\sunflower_pesticide_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=860,y=450)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\sunflower_pest.jpeg")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()

    def wheatpesticide():
        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebgpest.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=10,y=450)

        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\wheat_pesticide.png")
        p36=ImageTk.PhotoImage(i36)

        l=Label(top4,image=p36)
        l.place(x=600,y=450)

        i34=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\wheat_pesticide_det.png")
        p34=ImageTk.PhotoImage(i34)

        l=Label(top4,image=p34)
        l.place(x=900,y=480)
        
        i33=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\wheat_pest.jpg")
        p33=ImageTk.PhotoImage(i33)

        l=Label(top4,image=p33)
        l.place(x=230,y=450)
        
        top4.mainloop()
    
    i27=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\paddy.jpg")
    p27=ImageTk.PhotoImage(i27)
    b=Button(top4,image=p27,command=paddypesticide)
    b.place(x=50,y=150)
    
    
    i28=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\maize.jpg")
    p28=ImageTk.PhotoImage(i28)
    b=Button(top4,image=p28,command=maizepesticide)
    b.place(x=300,y=160)
    
    
    i29=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\groundnut.jpg")
    p29=ImageTk.PhotoImage(i29)
    b=Button(top4,image=p29,command=groundnutpesticide)
    b.place(x=550,y=150)
    
    
    i30=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\cotton.jpg")
    p30=ImageTk.PhotoImage(i30)
    b=Button(top4,image=p30,command=cottonpesticide)
    b.place(x=800,y=150)

    i31=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\sunflower.jpg")
    p31=ImageTk.PhotoImage(i31)
    b=Button(top4,image=p31,command=sunflowerpesticide)
    b.place(x=1050,y=150)

    i32=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\fertilizers section\wheat.jpg")
    p32=ImageTk.PhotoImage(i32)
    b=Button(top4,image=p32,command=wheatpesticide)
    b.place(x=1300,y=150)
    
    l=Label(top4,text="PADDY",font="arial 12 bold").place(x=120,y=290)
    l=Label(top4,text="MAIZE",font="arial 12 bold").place(x=370,y=290)
    
    l=Label(top4,text="GROUNDNUT",font="arial 12 bold").place(x=600,y=290)
    l=Label(top4,text="COTTON",font="arial 12 bold").place(x=850,y=290)
    l=Label(top4,text="SUNFLOWER",font="arial 12 bold").place(x=1100,y=290)
    l=Label(top4,text="WHEAT",font="arial 12 bold").place(x=1350,y=290)

    
    top4.mainloop()


   #crop market___________________________________________________________________________________________________________

def cropmarket():
    top5 = Toplevel()
    top5.geometry("1500x1000")
    top5.title("AGRO INDIA")

    i = Image.open(r"C:/Users/meenu/OneDrive/Pictures/Desktop/iomp/rtp/images/top5_bg.jpg")
    p = ImageTk.PhotoImage(i)
    l = Label(top5, image=p)
    l.image = p
    l.place(x=0, y=0)

    Label(top5, text="MARKET RATES", font="billyargel 24 bold", fg="black", bg="lightblue", padx=600).place(x=20, y=40)
    Label(top5, text="Click below to view live market prices:", font="billyargel 16 bold", fg="black", bg="lightgreen").place(x=20, y=120)

    def open_market_site():
        webbrowser.open("https://www.oneindia.com/vegetables-price.html")
    def open_agmarknet_site():
        webbrowser.open("https://agmarknet.gov.in/")

    Button(top5, text="View Agmarknet Prices", font=("Arial", 14), bg="lightgreen", command=open_agmarknet_site).place(x=300, y=180)

    Button(top5, text="View Live Market Prices", font=("Arial", 14), bg="lightgreen", command=open_market_site).place(x=50, y=180)

    top5.mainloop()



    #modern techniques_____________________________________________________________________________________________________________________________
def modern():
    top6=Toplevel()
    top6.geometry("1500x1000")
    top6.title("AGRO INDIA")
    l=Label(top6,text="MODERN TECHNOLOGY IN THE FIELD OF AGRICULTURE",font="billyargel 24 bold",fg="black",bg="lightgreen",padx=400).place(x=10,y=40)
    l=Label(top6,text="SELECT THE FIELD:",font="billyargel 16 bold",fg="black").place(x=20,y=116)

    def seeding():

        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg1.jpg")
        p36=ImageTk.PhotoImage(i36)
        l=Label(top6,image=p36)
        l.place(x=400,y=130)
        l=Label(top6,text="SEED DRILL",font="arial 20 bold",padx=10,width=20,bg="black",fg="white").place(x=750,y=200)

        i38=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\seeding_technique.jpg")
        p38=ImageTk.PhotoImage(i38)
        l=Label(top6,image=p38)
        l.place(x=680,y=250)
        l=Label(top6,text="ADVANTAGES :\n\n Precision Planting,Time Efficiency,reduced labour cost,\n\n increased productivity,customization options,sustainability ",font="helvetica 15 bold",width=70,bg="black",fg="white",pady=10).place(x=490,y=590)
        def open_seeding_video():
            webbrowser.open("https://youtu.be/WygacroTB8g?si=iAX6hfVyZ1yoRIw_")  # replace with actual link
        Button(top6, text="Watch on YouTube", font=("Arial", 12), bg="orange", command=open_seeding_video).place(x=800, y=800)
        top6.mainloop()

    def irrigation():

        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg1.jpg")
        p36=ImageTk.PhotoImage(i36)
        l=Label(top6,image=p36)
        l.place(x=400,y=130)
        l=Label(top6,text="SPRINKLERS",font="arial 20 bold",padx=10,width=20,bg="black",fg="white").place(x=750,y=200)

        i38=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\irrigation_technique.jpg")
        p38=ImageTk.PhotoImage(i38)
        l=Label(top6,image=p38)
        l.place(x=680,y=250)
        l=Label(top6,text="ADVANTAGES :\n\n Efficient Water Distribution,Time-Saving,Consistent Watering,\n\n Water Conservation,Improved Plant Health,sustainability ",width=70,bg="black",fg="white",font="helvetica 15 bold",pady=10).place(x=490,y=590)
        def open_irrigation_video():
            webbrowser.open("https://youtu.be/Z9HAy9EYKKs?si=1G6PlnVeY_4qruzd")  # replace with actual link
        Button(top6, text="Watch on YouTube", font=("Arial", 12), bg="orange", command=open_irrigation_video).place(x=800, y=800)
        top6.mainloop()

    def spraying():
        
        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg1.jpg")
        p36=ImageTk.PhotoImage(i36)
        l=Label(top6,image=p36)
        l.place(x=400,y=130)
        l=Label(top6,text="DRONES",font="arial 20 bold",padx=10,width=20,bg="black",fg="white").place(x=750,y=200)

        i38=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\spraying_technique.jpg")
        p38=ImageTk.PhotoImage(i38)
        l=Label(top6,image=p38)
        l.place(x=680,y=250)
        
        l=Label(top6,text="ADVANTAGES :\n\n Precision Application,Time Efficiency,Cost Savings,\n\n Environmental Benefits,Improved Crop Health Monitoring,Reduced Human Exposure ",width=70,bg="black",fg="white",font="helvetica 15 bold",pady=10).place(x=490,y=590)
        def open_spraying_video():
            webbrowser.open("https://youtu.be/JwWlnYmHlcI?si=KPh2LtvEhXqj6xVL")  # replace with actual link

        Button(top6, text="Watch on YouTube", font=("Arial", 12), bg="orange", command=open_spraying_video).place(x=800, y=800)

        top6.mainloop()

    def harvesting():
        
        i36=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\whitebg1.jpg")
        p36=ImageTk.PhotoImage(i36)
        l=Label(top6,image=p36)
        l.place(x=400,y=130)
        l=Label(top6,text="MULTI-USE HARVESTORS",font="arial 20 bold",padx=10,width=20,bg="black",fg="white").place(x=750,y=200)

        i38=Image.open(r"C:\Users\meenu\OneDrive\Pictures\Desktop\iomp\rtp\images\harvesting_technique.jpg")
        p38=ImageTk.PhotoImage(i38)
        l=Label(top6,image=p38)
        l.place(x=680,y=250)
        
        l=Label(top6,text="ADVANTAGES :\n\n Labor Savings,Cost Efficiency,Versatility,\n\n Enhanced Productivity,Technological Integration,Reduced Human Exposure ",font="helvetica 15 bold",pady=10,width=70,bg="black",fg="white").place(x=490,y=590)
        def open_harvesting_video():
            webbrowser.open("https://youtu.be/kWd_QnyO3eI?si=UNrNf09eGazBsO6g")  # replace with actual link

        Button(top6, text="Watch on YouTube", font=("Arial", 12), bg="orange", command=open_harvesting_video).place(x=800, y=800)

        top6.mainloop()
    
    b=Button(top6,text="SEEDING TECCHNIQUES",bg="lightblue",font="billyargel 15 bold",width=30,command=seeding).place(x=20,y=170)
    b=Button(top6,text="IRRIGATION TECHNIQUES",bg="lightblue",font="billyargel 15 bold",width=30,command=irrigation).place(x=20,y=270)
    b=Button(top6,text="SPRAYING TECHNIQUES",bg="lightblue",font="billyargel 15 bold",width=30,command=spraying).place(x=20,y=370)
    b=Button(top6,text="HARVESTING TECHNIQUES",bg="lightblue",font="billyargel 15 bold",width=30,command=harvesting).place(x=20,y=470)

b=Button(top,text="crop suggestion",font="arial 15 bold",width=20,bg="lightblue",command=crop).place(x=120,y=570)
b=Button(top,text="fertilizers ",font="arial 15 bold",width=20,bg="lightblue",command=fertilizer).place(x=490,y=570)
b=Button(top,text="pesticides",font="arial 15 bold",width=20,bg="lightblue",command=pesticide).place(x=830,y=570)

b=Button(top,text="crop market",font="arial 15 bold",width=20,bg="lightblue",command=cropmarket).place(x=1150,y=570)
b=Button(top,text="modern techniques",font="arial 15 bold",width=20,bg="lightblue",command=modern).place(x=490,y=670)
b = Button(top, text="Agro ChatBot", font="arial 15 bold", width=20, bg="lightblue", command=chatbot).place(x=830,y=670)
top.mainloop()
