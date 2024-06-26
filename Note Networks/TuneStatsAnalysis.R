library(tidyverse)
library(igraph)

# ------------------ just working on tune stats----
tune_stats <-  read_csv("Tune Stats.csv", col_names = TRUE)

tune_stats %>% arrange(desc(clustcoef) )
tune_stats %>% arrange(clustcoef)
tune_stats %>% filter(!is.na(diameter)) %>% arrange(diameter)
tune_stats %>% arrange(desc(diameter))

sum(tune_stats$connected)

mean(tune_stats$diameter[!is.na(tune_stats$diameter)])
# --------------------------------------------------

numcon <- 0
n <- 100000

for (i in 1:n){
  currname = sample(tune_stats$name, 1)
  v <- tune_stats$numUniqueNotes[tune_stats$name == currname]
  e <-  tune_stats$numEdges[tune_stats$name == currname]
  g <- erdos.renyi.game(v,e,type="gnm", directed = TRUE, loops = TRUE)
  if (is_connected(g, mode="strong")){
    numcon <- numcon+1
  }
}

numcon/n

sum(tune_stats$connected)/length(tune_stats$connected)

#--------------------- connectedness ---------------


# ---------------------------------------------------------------
# ----------------------- diving things up by idiom ----
tune_info <- read_csv("~/MATHCOMP479/Project/TuneInfo.csv")

full_info <- inner_join(tune_info, tune_stats, join_by(Name == name))


full_info %>% group_by(Idiom) %>% summarise(mean(clustcoef), n())
full_info %>% filter(connected) %>% group_by(Idiom) %>% summarise(mean(diameter))
full_info %>% filter(connected) %>% group_by(Idiom) %>% summarise(mean(avgpathlen))
hist(sort(full_info$diameter[full_info$connected]))

full_info %>% group_by(Idiom)%>% summarise(sum(connected))
full_info %>% group_by(Idiom)%>% summarise(n())

full_info %>% filter(NumParts > 0 & NumParts <= 6) %>% group_by(NumParts) %>% summarise(mean(clustcoef))
hist(full_info$NumParts[full_info$NumParts > 0 & full_info$NumParts <= 6])
# -------------------------------------------------------


# ------------------- overall tune networks
idiom_stats <- read_csv("Idiom Stats.csv")
idiom_stats
# -----------------------------------------
