import cv2
import json

# === 1. Load gambar (ambil dari video frame pertama kalau perlu) ===
image_path = 'E:/projek_perancangan2/frame9.jpg'  # ganti ke file kamu
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(f"Gambar tidak ditemukan di {image_path}")

clone = image.copy()
slots = {}
slot_count = 0
click_points = []  # menyimpan sementara 2 titik per slot

# === 2. Callback mouse untuk klik koordinat ===
def select_point(event, x, y, flags, param):
    global slot_count, click_points
    if event == cv2.EVENT_LBUTTONDOWN:
        click_points.append((x, y))
        cv2.circle(clone, (x, y), 5, (0, 0, 255), -1)

        # Kalau sudah 2 titik, simpan sebagai 1 slot
        if len(click_points) == 2:
            slot_count += 1
            slot_name = f"A{slot_count}"

            # Simpan ke dict: "A1": [[x1,y1],[x2,y2]]
            slots[slot_name] = click_points.copy()

            # Gambar kotaknya
            (x1, y1), (x2, y2) = click_points
            cv2.rectangle(clone, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(clone, slot_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            click_points = []  # reset untuk slot berikutnya
            cv2.imshow("Mapping Slot Parkir", clone)
        else:
            cv2.imshow("Mapping Slot Parkir", clone)

# === 3. Buka jendela untuk klik titik-titik slot ===
cv2.imshow("Mapping Slot Parkir", clone)
cv2.setMouseCallback("Mapping Slot Parkir", select_point)

print("Klik dua kali (kiri atas dan kanan bawah) untuk tiap slot parkir.")
print("Tekan 's' untuk save, atau 'q' untuk keluar tanpa menyimpan.")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        with open('E:/projek_perancangan2/slots7.json', 'w') as f:
            json.dump(slots, f, indent=4)
        print(" Koordinat disimpan ke slots7.json")
        break
    elif key == ord('q'):
        print(" Dibatalkan tanpa menyimpan")
        break

cv2.destroyAllWindows()
