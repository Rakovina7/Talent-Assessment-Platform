import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore, auth
import importlib

# Initialize Firebase
cred = credentials.Certificate('C:\\Users\\Etern\\OneDrive\\Masaüstü\\Hackathon\\credintails.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Constants for UI
WINDOW_TITLE = "Yetenek Değerlendirme Platformu"
FONT_MAIN = ("Arial", 12, "bold")
BACKGROUND_COLOR = "#333333"
TEXT_COLOR = "#FFFFFF"
BUTTON_COLOR = "#0078D7"
BUTTON_TEXT_COLOR = "#FFFFFF"
INPUT_BG_COLOR = "#1F1F1F"
INPUT_FG_COLOR = "#FFFFFF"
PADX = 20
PADY = 20

# Register user in Firebase Authentication
def register_user(email, password, isim, soyisim):
    try:
        user = auth.create_user(email=email, password=password)
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({'isim': isim, 'soyisim': soyisim})
        messagebox.showinfo("Başarılı", "Giriş başarılı, oyun ekranına yönlendiriliyorsunuz.")
        return user.uid
    except Exception as e:
        print(f"Error creating user: {e}")
        messagebox.showerror("Hata", "Kayıt sırasında bir hata oluştu.")
        return None
    
# Save scores in Firestore
def skorlari_kaydet(uid, email, isim, soyisim, oyun_skor, score):
    doc_ref = db.collection('kullanici_skorlari').document(uid)
    current_data = doc_ref.get().to_dict() if doc_ref.get().exists else {}
    current_data[f'Oyun{oyun_skor}_Skor'] = score
    current_data['Toplam_Skor'] = sum([current_data.get(f'Oyun{i}_Skor', 0) for i in range(1, 3)])
    current_data['Email'] = email
    current_data['Isim'] = isim
    current_data['Soyisim'] = soyisim
    doc_ref.set(current_data)
    print("Skorlar başarıyla kaydedildi.")

# Check if the game has been played
def oyunu_oynandi_mi(uid, oyun_skor):
    doc_ref = db.collection('kullanici_skorlari').document(uid)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return f'Oyun{oyun_skor}_Skor' in data and data[f'Oyun{oyun_skor}_Skor'] is not None
    return False

# Constants for games
GAME_TITLE = "Skor Oyunu"
BUTTON_TEXT_START = " için Başla"

# Modified game-playing function with additional arguments for game title and button text
def oyun_oyna(uid, email, isim, soyisim, oyun_no):
    try:
        # Import the game module using importlib
        game_module = importlib.import_module(f'games.game{oyun_no}')

        # Run the game, now passing the game title and button text
        game_module.run_game(uid, email, isim, soyisim, oyun_no, GAME_TITLE, BUTTON_TEXT_START)
    except ModuleNotFoundError:
        messagebox.showerror("Hata", f"Oyun {oyun_no} bulunamadı.")
        return
    except Exception as e:
        messagebox.showerror("Hata", f"Oyun yüklenirken bir hata oluştu: {e}")
        return

# GUI for game selection
def oyun_sec_arayuzu(isim, soyisim, email, password, ana_pencere):
    uid = register_user(email, password, isim, soyisim)
    if uid is None:
        return

    # Hide the main window instead of destroying it
    ana_pencere.withdraw()

    # Create the game selection window
    oyun_sec_pencere = tk.Toplevel()
    oyun_sec_pencere.title(WINDOW_TITLE)

    welcome_label = tk.Label(oyun_sec_pencere, text=f"Hoşgeldiniz {isim} {soyisim}", font=FONT_MAIN)
    welcome_label.pack(padx=PADX, pady=PADY)

    info_label = tk.Label(oyun_sec_pencere, text="Oyunları sırayla oynamanız gerekmektedir.\nBu platform, yetenek değerlendirmesi için bir test platformudur.", font=FONT_MAIN)
    info_label.pack(padx=PADX, pady=PADY)

    def oyun_baslat(oyun_no):
        if oyunu_oynandi_mi(uid, oyun_no):
            messagebox.showinfo("Bilgi", f"Oyun {oyun_no} zaten oynandı.")
            return

        if oyun_no > 1 and not oyunu_oynandi_mi(uid, oyun_no - 1):
            messagebox.showinfo("Bilgi", f"Lütfen önce Oyun {oyun_no - 1} oynayın.")
            return

        oyun_oyna(uid, email, isim, soyisim, oyun_no)

    buton_oyun1 = tk.Button(oyun_sec_pencere, text="Oyun 1" + BUTTON_TEXT_START, command=lambda: oyun_baslat(1), font=FONT_MAIN)
    buton_oyun1.pack(padx=PADX, pady=PADY)

    buton_oyun2 = tk.Button(oyun_sec_pencere, text="Oyun 2" + BUTTON_TEXT_START, command=lambda: oyun_baslat(2), font=FONT_MAIN)
    buton_oyun2.pack(padx=PADX, pady=PADY)

    oyun_sec_pencere.mainloop()
    ana_pencere.destroy()  # Destroy the main window when the game selection window is closed

# Main application window
def main_application_window():
    ana_pencere = tk.Tk()
    ana_pencere.title(WINDOW_TITLE)
    ana_pencere.configure(bg=BACKGROUND_COLOR)

    label_aciklama = tk.Label(ana_pencere, text="Lütfen İsim, Soyisim, Email ve Şifrenizi Girin",
                              font=FONT_MAIN, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    label_aciklama.pack(padx=PADX, pady=PADY)

    label_isim = tk.Label(ana_pencere, text="İsim:", font=FONT_MAIN, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    label_isim.pack(padx=PADX, pady=PADY)
    isim_giris = tk.Entry(ana_pencere, font=FONT_MAIN, bg=INPUT_BG_COLOR, fg=INPUT_FG_COLOR)
    isim_giris.pack(padx=PADX, pady=PADY)

    label_soyisim = tk.Label(ana_pencere, text="Soyisim:", font=FONT_MAIN, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    label_soyisim.pack(padx=PADX, pady=PADY)
    soyisim_giris = tk.Entry(ana_pencere, font=FONT_MAIN, bg=INPUT_BG_COLOR, fg=INPUT_FG_COLOR)
    soyisim_giris.pack(padx=PADX, pady=PADY)

    label_email = tk.Label(ana_pencere, text="Email:", font=FONT_MAIN, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    label_email.pack(padx=PADX, pady=PADY)
    email_giris = tk.Entry(ana_pencere, font=FONT_MAIN, bg=INPUT_BG_COLOR, fg=INPUT_FG_COLOR)
    email_giris.pack(padx=PADX, pady=PADY)

    label_password = tk.Label(ana_pencere, text="Şifre:", font=FONT_MAIN, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    label_password.pack(padx=PADX, pady=PADY)
    password_giris = tk.Entry(ana_pencere, show='*', font=FONT_MAIN, bg=INPUT_BG_COLOR, fg=INPUT_FG_COLOR)
    password_giris.pack(padx=PADX, pady=PADY)

    gonder_buton = tk.Button(ana_pencere, text="Başla", command=lambda: oyun_sec_arayuzu(isim_giris.get(), soyisim_giris.get(), email_giris.get(), password_giris.get(), ana_pencere), font=FONT_MAIN, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    gonder_buton.pack(padx=PADX, pady=PADY)

    return ana_pencere

if __name__ == "__main__":
    app = main_application_window()
    app.mainloop()