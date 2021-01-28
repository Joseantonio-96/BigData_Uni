#install.packages("tidyverse")
#install.packages("tidyr")
#install.packages("cluster")
#install.packages("purrr")
#install.packages("foreach")

library(tidyverse)
library(tidyr)
library(cluster)
library(purrr)
library(parallel)
library(foreach)
library(doParallel)

# start timer
starttime = Sys.time()

#Importing data
data = read.csv("computers.csv", sep = ";", stringsAsFactors = F, fileEncoding="latin1")
colnames(data)[1] <- 'id'

#transforming data
data <- data %>%
  mutate(cd = ifelse(cd =="yes", 1, 0), multi = ifelse(multi =="yes", 1, 0), premium = ifelse(premium =="yes", 1, 0))

computers_new = subset(data, select = -c(id) )

# Use map_dbl to run many models with varying value of k (centers)
tot_withinss <- map_dbl(1:10,  function(k){
  model <- kmeans(x = computers_new, centers = k)
  model$tot.withinss
})

# Generate a data frame containing both k and tot_withinss
elbow_df <- data.frame(k = 1:10, tot_withinss = tot_withinss)

# Plot the elbow plot
ggplot(elbow_df, aes(x = k, y = tot_withinss)) +
  geom_line(color = "darkorchid1", size=1)+
  geom_point(colour=1, size=1)+
  theme(plot.title = element_text(hjust=0.5))+
  scale_x_continuous(breaks = 1:20)+
  labs(title = "Elbow Plot", adj= 0.5, line=2)+
  xlab("Number of Clusters k") +
  ylab("Within-cluster sum of squares (Inertia)") 

#Cluster the data using the optimum value using k-means. 
# (Manually change this value to select a different number of clusters)
NUM_CLUSTERS = 4
model_km2 <-kmeans(computers_new, NUM_CLUSTERS)
computers_new_clustered <- mutate(computers_new, cluster = model_km2$cluster)

#Plot the first 2 dimensions of the clusters
plot(model_km2$centers[,1], model_km2$centers[,2], main="Cluster centers for first 2 dimensions", xlab = colnames(model_km2$centers)[1], ylab=colnames(model_km2$centers)[2]) 

#selecting centroids
centroids <- data.frame(model_km2$centers)

# Plot the heat map
# Scale the values to add visibility to the plot
centroids_scaled <- data.frame("Scaled_Price" = centroids$price/1000, "Scaled_Speed" = centroids$speed/10, "Scaled_HD" = centroids$hd/100, "Ram" = centroids$ram, 
                               "Scaled_Screen" = centroids$screen/10, "Scaled_CD" = centroids$cd*10, "Scaled_Multi" = centroids$multi*10, "Scaled_Premium" = centroids$premium*10,
                               "Scaled_Ads" = centroids$ads/100, "Trend" = centroids$trend)

# Reshape the dataframe to be able to plot the heat map
heat_data <- centroids_scaled %>% 
  rownames_to_column() %>%
  gather(colname, value, -rowname)

# Plotting the heat map
ggplot(heat_data, aes(x = rowname, y = colname, fill = value)) + 
  geom_tile()

endtime = Sys.time()

# Getting cluster average and printing the highest one
Custer_avgs<- computers_new_clustered %>% group_by(cluster) %>% summarise(mean = mean(price))
print(paste("Cluster with highest price average is:", max(Custer_avgs[,2])))

print('Total time is:')
endtime - starttime
