library(tidyverse)

# ------------------ just working on tune stats----
tune_stats <-  read_csv("Tune Stats.csv", col_names = TRUE)

tune_stats %>% arrange(desc(clustcoef) )
tune_stats %>% arrange(clustcoef)
tune_stats %>% filter(diameter>0) %>% arrange(diameter)
tune_stats %>% arrange(desc(diameter))

sum(tune_stats$connected)

mean(tune_stats$diameter[tune_stats$diameter > 0])
# --------------------------------------------------



tune_info <- read_csv("~/MATHCOMP479/Project/TuneInfo.csv")

full_info <- inner_join(tune_info, tune_stats, join_by(Name == name))


full_info %>% group_by(Idiom) %>% summarise(mean(clustcoef))
full_info %>% filter(connected) %>% group_by(Idiom) %>% summarise(mean(diameter))
full_info %>% filter(connected) %>% group_by(Idiom) %>% summarise(mean(avgpathlen))
hist(sort(full_info$diameter[full_info$connected]))




full_info %>% filter(NumParts > 0 & NumParts <= 6) %>% group_by(NumParts) %>% summarise(mean(clustcoef))
hist(full_info$NumParts[full_info$NumParts > 0 & full_info$NumParts <= 6])
