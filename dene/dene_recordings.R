# plot sampling density based on CSV files with metadata on recording dates, lengths of recordings, and target children
# usage: put script in same folder as sessions.csv and participants.csv; run source(dene_recordings.R, chdir=T)

library(ggplot2)

# convert "HH:MM:SS" to minutes as number
time_as_minutes <- function(full_time){
	full_time = strptime(full_time, format="%H:%M:%S")
	minutes = full_time$hour*60 + full_time$min # + full_time$sec
	return(minutes)
}

# convert number of days to YY;MM.DD
days_as_age <- function(days_to_consider){
	remainder = days_to_consider %% 365
	years = (days_to_consider  - remainder) / 365
	days_to_consider = remainder
	remainder = days_to_consider %% (365/12)
	months = (days_to_consider - remainder) / (365/12)
	days = round(remainder)
	age = paste(years, ";", months, ".", days, sep="")
	return(age)
}

# set working directory to path from where script was called
# setwd(dirname(sys.frame(1)$ofile))

# read and prepare session data
read.csv("sessions.csv") -> sessions
sessions <- sessions[,c("Code","Date","Length.of.recording")]
# replace session code by code of target child
sessions$Code <- gsub("^.*-([A-Z]+)-.*$","\\1",sessions$Code)
# replace "." by "-" in Date column to get YYYY-MM-DD
sessions$Date <- gsub("\\.","-",sessions$Date)
sessions$Date <- as.Date(sessions$Date)
# convert length of recording to numeric minutes
sessions$Length.of.recording <- time_as_minutes(sessions$Length.of.recording)

# read and prepare participant data
read.csv("participants.csv") -> participants
participants <- participants[,c("Short.name","Birth.date")]
# replace "." by "-" in Date column to get YYYY-MM-DD
participants$Birth.date <- gsub("\\.","-",participants$Birth.date)
participants$Birth.date <- as.Date(participants$Birth.date)

# merge dataframes
sessions_complete <- merge(sessions, participants, by.x="Code", by.y="Short.name")
# calculate age
sessions_complete$Age_in_days <- as.numeric(sessions_complete$Date - sessions_complete$Birth.date)

# create plot
# get vectors for ticks and labels on x axis
ages_in_days = seq(from=min(sessions_complete$Age_in_days), to=max(sessions_complete$Age_in_days)+30, by=30)
ages_formatted = days_as_age(ages_in_days)
# vector to scale size of points
size_scaling = seq(from=round(min(sessions_complete$Length.of.recording),-1), to=round(max(sessions_complete$Length.of.recording),-1), by=30)
# plot
p <- ggplot(sessions_complete, aes(x=Age_in_days, y=reorder(Code, Age_in_days, min), colour=Code, size=Length.of.recording)) + 
	ggtitle("Length and density of DESLAS recordings") +
	xlab("Age in days") + 
	scale_x_continuous(breaks=ages_in_days, labels=ages_formatted) + 
	ylab("Children sorted by start of recordings") + 
	labs(size="Length of recording\nin minutes") + 
	scale_size(breaks=size_scaling) +
	geom_point()
plot(p)