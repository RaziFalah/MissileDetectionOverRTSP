import matplotlib.pyplot as plt

# Time stamps in seconds (from your log)
timestamps = [
    0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,
    10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0,
    20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0
]

# Corresponding audio volumes
audio_volumes = [
    0.0000, 0.0023, 0.0018, 0.0004, 0.0008, 0.0024, 0.0015, 0.0006, 0.0003, 0.0006,
    0.0007, 0.0002, 0.0007, 0.0024, 0.0012, 0.0001, 0.0028, 0.0017, 0.0007, 0.0002,
    0.0000, 0.0015, 0.0029, 0.0027, 0.0028, 0.0020, 0.0014, 0.0007
]

plt.figure(figsize=(10, 4))
plt.plot(timestamps, audio_volumes, marker='o')
plt.title('Audio Volume Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Audio Volume')
plt.grid(True)
plt.tight_layout()
plt.show()