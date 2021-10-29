(ns my-sketch.test
    (:require [quil.core :as q]
              [quil.middleware :as m]))
  
  (defn setup []
    ; Set frame rate to 30 frames per second.
    (q/frame-rate 30)
    ; Set color mode to HSB (HSV) instead of default RGB.
    (q/color-mode :hsb)
    (q/background 0)
    ; setup function returns initial state. It contains
    ; circle color and position.
    {:t 0})
  
  (defn update-state [state]
    {:t (mod (+ (:t state) (q/random 5 20)) (q/height))})
  
  (defn draw-state [state]
    ; Calculate x and y coordinates of the circle.
    (q/stroke (q/random 255) 255 255)
    (q/no-fill)
    (let [t (:t state) 
      m (/ (q/width) 2)
      s (/ m 2)]
        (q/bezier 0 t 
          (+ m (* s (q/random-gaussian))) (+ m (* s (q/random-gaussian)))  
          (+ m (* s (q/random-gaussian))) (+ m (* s (q/random-gaussian)))  
          t (q/width))))
  
  
  (q/defsketch my-sketch
    :title "TEST TEST TEST"
    :size [500 500]
    ; setup function called only once, during sketch initialization.
    :setup setup
    ; update-state is called on each iteration before draw-state.
    :update update-state
    :draw draw-state
    :features [:keep-on-top]
    ; This sketch uses functional-mode middleware.
    ; Check quil wiki for more info about middlewares and particularly
    ; fun-mode.
    :middleware [m/fun-mode])
  