#install.packages("tidyverse")
#install.packages("tidyr")
#install.packages("cluster")
#install.packages("purrr")
#install.packages("foreach")
#install.packages("Matrix")

library(tidyverse)
library(tidyr)
library(cluster)
library(purrr)
library(parallel)
library(doParallel)
library(foreach)
library(lme4)

startTime = Sys.time()

#Importing data
data = read.csv("computers.csv", sep = ";", stringsAsFactors = F, fileEncoding="latin1")
colnames(data)[1] <- "Id"
#transforming data
data <- data %>%
  mutate(cd = ifelse(cd =="yes", 1, 0), multi = ifelse(multi =="yes", 1, 0), premium = ifelse(premium =="yes", 1, 0))

data_new = subset(data, select = - c(Id) )


# define the function
k_clust = 1:10
createCluster <- function(k){
  model <- kmeans(x = data_new, centers = k, iter.max = 100)
  return(model$tot.withinss)
}

cl_withinss = mclapply(k_clust, createCluster)


# Generate a data frame containing both k and tot_withinss
elbow_df <- data.frame(k = k_clust, cl_withinss = cl_withinss)

# Plot the elbow plot
Inertia <- as.numeric(cl_withinss)
ggplot(elbow_df, aes(x = k_clust, y = Inertia)) +
  geom_line(color = "darkorchid1", size=1)+
  geom_point(colour=1, size=1)+
  theme(plot.title = element_text(hjust=0.5))+
  scale_x_continuous(breaks = 1:20)+
  labs(title = "Elbow Plot", adj= 0.5, line=2)+
  xlab("Number of clusters k") +
  ylab("Within-cluster sum of squares (Inertia)") 

#Cluster the data using the optimum value using k-means.
NUM_CLUSTERS = 4
kmeansModel <-kmeans(data_new, NUM_CLUSTERS)
data_clusters_selected<- mutate(data_new, cluster = kmeansModel$cluster)

#Plot the first 2 dimensions of the clusters
plot(kmeansModel$centers[,1], kmeansModel$centers[,2], main="Cluster centers for first 2 dimensions", xlab = colnames(kmeansModel$centers)[1], ylab=colnames(kmeansModel$centers)[2]) 

#selecting centroids
centroids <- data.frame(kmeansModel$centers)

# Plot the heat map
# Scale the values to add visibility to the plot
centroids_scaled <- data.frame("Scaled_Price" = centroids$price/1000, "Scaled_Speed" = centroids$speed/10, "Scaled_HD" =centroids$hd/100, "Ram" = centroids$ram, 
                               "Scaled_Screen" = centroids$screen/10, "Scaled_CD" = centroids$cd*10, "Scaled_Multi" = centroids$multi*10, "Scaled_Premium" = centroids$premium*10,
                               "Scaled_Ads" = centroids$ads/100, "Trend" = centroids$trend)

# Reshape the dataframe to be able to plot the heat map
heat_data <- centroids_scaled %>% 
  rownames_to_column() %>%
  gather(colname, value, -rowname)

# Plotting the heat map
ggplot(heat_data, aes(x = rowname, y = colname, fill = value)) + 
  geom_tile()

endTime = Sys.time()

# Getting cluster average and printing the highest one
Custer_avgs <- data_clusters_selected %>% group_by(cluster) %>% summarize(mean = mean(price))
print(paste("Cluster with highest price average is:", max(Custer_avgs[,2])))

print("Total time to perform process is:")
endTime - startTime
