(ns quil-intro
  (:require [quil.core :as q]))

(defn f [t]
  [(* t (q/sin t))
   (* t (q/cos t))])

(defn f2 [t]
  (let [r (* 200 (q/sin t) (q/cos t))]
    [(* r (q/sin (* t 0.2)))
     (* r (q/cos (* t 0.2)))]))

(defn draw-plot [f from to step]
  (doseq [two-points (->> (range from to step)
                          (map f)
                          (partition 2 1))]
        ; we could use 'point' function to draw a point
        ; but let's rather draw a line which connects 2 points of the plot
    (apply q/line two-points)))

(defn draw []
  (q/with-translation [(/ (q/width) 2) (/ (q/height) 2)]
        ; note that we don't use draw-plot here as we need
        ; to draw only small part of a plot on each iteration
    (let [t (/ (q/frame-count) 10)]
      (q/line (f2 t)
              (f2 (+ t 0.1))))))

    ; 'setup' is a cousin of 'draw' function
    ; setup initialises sketch and it is called only once
    ; before draw called for the first time
(defn setup []
      ; draw will be called 60 times per second
  (q/frame-rate 60)
      ; set background to white colour only in the setup
      ; otherwise each invocation of 'draw' would clear sketch completely
  (q/background 255))

(q/defsketch trigonometry
  :size [300 300]
  :setup setup
  :draw draw)