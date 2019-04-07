#! /path/to/Rscript

library(stats)
library(strucchange)

topic_times <- read.table("./models/db/topic_times.csv", header=F, sep=",")
time_start <- read.table("./models/db/time-seq.txt", header=F)
col <- length(topic_times[1,])-2
topic_num <- c(1:col)


####################################################################
# (1)以下部分对strucchange_topic进行绘图

for(i in topic_num){

  svg(file=paste("./results/strucchange_topic",as.character(i-1),".svg"),width=12, height=8)

  prob <- ts(topic_times[,i], start=c(as.numeric(time_start[1,1])), frequency=1)

  # store the breakdates
  bp_ts <- breakpoints(prob~1)

  # this will give you the break dates and their confidence intervals
  summary(bp_ts)

  # to plot the breakpoints with confidence intervals
  # plot(prob,main=paste("Topic",as.character(i-1)),lwd=2)

  # 修改图片边距，即oma和mar后面的值，方向为“左、下、右、上”
  par(oma=c(4,2,2,2), mar=c(4,4,2,2))
  plot(prob, ann = F, xaxt = "n", yaxt = "n", lwd=2)
  lines(bp_ts)

  # 以下部分为显示均值线
  bdate <- breakdates(bp_ts)
  ptr <- c()
  for(bd in bdate){
    ptr <- c(ptr, which(time_start[,1] == bd))
  }
  idx <- 1
  for(p in ptr){
    x <- c(time_start[idx, 1], time_start[p, 1])
    y <- c(mean(prob[idx:p]), mean(prob[idx:p]))
    # 设置分区均值线的粗细，修改lwd参数
    lines(x, y, lwd=1)
    idx <- p
  }
  x <- c(time_start[idx, 1], time_start[length(prob)-1, 1])
  y <- c(mean(prob[idx:length(prob)]), mean(prob[idx:length(prob)]))
  # 设置分区均值线的粗细，修改lwd参数
  lines(x, y, lwd=1)

  a <- c(time_start[1,1], time_start[length(prob)-1, 1])
  b <- c(mean(prob), mean(prob))
  # 设置整体均值线的粗细，修改lwd参数
  lines(a, b, lwd=2)

  axis(side=1, tcl=0.5, cex.axis=1)
  axis(side=2, tcl=0.5, cex.axis=1)
  title(xlab= 'Year', ylab = 'Probability',line = 3)

  dev.off()
}

#########################################################################
# (2)以下部分对topic-time_std_strucchange进行绘图
svg(file=paste("./results/topic_time_std_strucchange.svg"),width=12, height=8)
prob <- ts(topic_times[,length(topic_times[1,])], start=c(as.numeric(time_start[1,1])), frequency=1)
bp_ts <- breakpoints(prob~1)
summary(bp_ts)

# 修改图片边距，即oma和mar后面的值，方向为“左、下、右、上”
par(oma=c(4,2,2,2), mar=c(4,4,2,2))
plot(prob, ann = F, xaxt = "n", yaxt = "n", lwd=2)

lines(bp_ts)

c <- c(time_start[1,1], time_start[length(prob)-1, 1])
d <- c(topic_times[1,length(topic_times[1,])-1], topic_times[1,length(topic_times[1,])-1])
lines(c, d, lwd=2)

# 以下部分为显示均值线
  bdate <- breakdates(bp_ts)
  ptr <- c()
  for(bd in bdate){
    ptr <- c(ptr, which(time_start[,1] == bd))
  }
  idx <- 1
  for(p in ptr){
    x <- c(time_start[idx, 1], time_start[p, 1])
    y <- c(mean(prob[idx:p]), mean(prob[idx:p]))
    # 设置分区均值线的粗细，修改lwd参数
    lines(x, y, lwd=1)
    idx <- p
  }
  x <- c(time_start[idx, 1], time_start[length(prob)-1, 1])
  y <- c(mean(prob[idx:length(prob)]), mean(prob[idx:length(prob)]))
  # 设置分区均值线的粗细，修改lwd参数
  lines(x, y, lwd=1)
  e <- c(time_start[1,1], time_start[length(prob)-1, 1])
  f <- c(mean(prob), mean(prob))
  # 设置整体均值线的粗细，修改lwd参数
  lines(e, f, lwd=1)

axis(side=1, tcl=0.5, cex.axis=1)
axis(side=2, tcl=0.5, cex.axis=1)
title(xlab= 'Year', ylab = 'Mean & Standard deviation',line = 3)
dev.off()

####################################################################
# (3)以下部分对word-time_std_strucchange进行绘图
for(i in topic_num){

  word_times <- read.table(paste("./models/db/word-times_topic",as.character(i-1),".csv", sep=""), header=F, sep=",")
  svg(file=paste("./results/word_time_std_strucchange_topic",as.character(i-1),".svg"),width=12, height=8)

  row <- length(word_times[,1])
  col <- length(word_times[1,])
  wt <- as.numeric(word_times[row, 2:col])
  prob <- ts(wt, start=c(as.numeric(time_start[1,1])), frequency=1)
  bp_ts <- breakpoints(prob~1)

  # 修改图片边距，即oma和mar后面的值，方向为“左、下、右、上”
  par(oma=c(4,2,2,2), mar=c(4,4,2,2))
  plot(prob, ann = F, xaxt = "n", yaxt = "n", lwd=2)

  lines(bp_ts)

  # 以下部分为显示均值线
  bdate <- breakdates(bp_ts)
  ptr <- c()
  for(bd in bdate){
    ptr <- c(ptr, which(time_start[,1] == bd))
  }
  idx <- 1
  for(p in ptr){
    x <- c(time_start[idx, 1], time_start[p, 1])
    y <- c(mean(prob[idx:p]), mean(prob[idx:p]))
    # 设置分区均值线的粗细，修改lwd参数
    lines(x, y, lwd=1)
    idx <- p
  }
  x <- c(time_start[idx, 1], time_start[length(prob)-1, 1])
  y <- c(mean(prob[idx:length(prob)]), mean(prob[idx:length(prob)]))
  # 设置分区均值线的粗细，修改lwd参数
  lines(x, y, lwd=1)

  a <- c(time_start[1,1], time_start[length(prob)-1, 1])
  b <- c(mean(prob), mean(prob))
  # 设置整体均值线的粗细，修改lwd参数
  lines(a, b, lwd=2)

  axis(side=1, tcl=0.5, cex.axis=1)
  axis(side=2, tcl=0.5, cex.axis=1)
  title(xlab = 'Year', ylab = 'Standard deviation',line = 3)

  dev.off()
}