(ns blottsbooks.core
  (:gen-class))

(defn say-welcome [what]
  (println "Welcome to" what "!"))

(defn -main
  [& args]
  (say-welcome "Blotts Books"))