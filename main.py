import threading
import queue
import time

# 全局變量
frame_queue = queue.Queue(maxsize=1)
stop_event = threading.Event()

def capture_thread():
    while not stop_event.is_set():
        ret, image = cap.read()
        if ret:
            if frame_queue.full():
                frame_queue.get()
            frame_queue.put(image)
        else:
            break

def main():
    global cap, hands, keypoint_classifier_R, keypoint_classifier_L, mouse_classifier, point_history_classifier

    # 初始化相機和模型
    # (這裡省略了原始程式碼中的初始化部分，保持不變)

    threading.Thread(target=capture_thread, daemon=True).start()

    target_fps = 30
    frame_time = 1 / target_fps

    while not stop_event.is_set():
        start_time = time.time()

        # Process Key (ESC: end)
        key = cv.waitKey(1)
        if key == 27:  # ESC
            stop_event.set()
            break
        number, mode = select_mode(key, mode)

        # 從隊列中獲取圖像
        if not frame_queue.empty():
            image = frame_queue.get()
        else:
            continue

        image = cv.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        # 檢測是否有手
        if results.multi_hand_landmarks is None:
            rest_id = 0
            rest_result.append(rest_id)
        if results.multi_hand_landmarks is not None:
            rest_id = 1
            rest_result.append(rest_id)
        most_common_rest_result = Counter(rest_result).most_common()

        # 檢查是否進入休眠模式
        if time.time() - resttime > 10:
            if detect_mode != 0:
                detect_mode = 0
                what_mode = 'Sleep'
                print(f'Current mode => {what_mode}')

        # 如果檢測到手
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # (這裡保持原有的手勢識別和處理邏輯不變)
                # ...

        # 檢測是否有手勢並執行相應操作
        if left_id + right_id > -2:
            # (這裡保持原有的模式切換和操作邏輯不變)
            # ...

        # 顯示當前模式
        cv.putText(debug_image, what_mode, (400, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)

        # 顯示處理後的影像
        cv.imshow('Hand Gesture Recognition', debug_image)

        # 控制幀率
        processing_time = time.time() - start_time
        if processing_time < frame_time:
            time.sleep(frame_time - processing_time)

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()