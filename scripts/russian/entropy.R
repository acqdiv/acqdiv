# Packages
library(ToolboxSearch)
library(entropy)
library(doBy)


# Loading toolbox files
########################
fmt <- toolboxFormat (
	utterance=c(ref,speaker,age),
	word=mor
)

# single File
# corpus <- readToolbox("A00110810.cha.txt",fmt) 
# corpus <- readToolbox(textConnection(gsub("\t", " ", readLines("A00110810.cha.txt"))),fmt) 

# all Files in a directory
files <- dir(path="/Users/lukaswiget/Documents/Projekte/Russisch_Entropie/chat2toolbox/toolbox_notabs", pattern="txt$", full.names=T)
corpora <- lapply(files, function(x) readToolbox(x,fmt))
corpus <- concat.corpus(corpora)


# Editing of corpus
##################
# delete Sabine's and Balthasar's utterances
corpus <- corpus[corpus %% "@utterance{NOT $speaker == 'SAB'}"]
corpus <- corpus[corpus %% "@utterance{NOT $speaker == 'BAL'}"]

# delete Anjas utterances (note: age not in filename and thus not easily transferable to adults) 
corpus <- corpus[corpus %% "@utterance{NOT $speaker == 'ANJ'}"]

# make a dataframe
ruscorp <- as.data.frame(corpus)
ruscorp$speaker <- as.factor(ruscorp$speaker)

# code adult vs. child
ruscorp$adult <-rep("child", length(ruscorp$ref))
ruscorp$adult[! ruscorp$speaker %in% c("ALJ","ANJ","JAS","PAS","VAN")] <- "adult"
ruscorp$adult <- as.factor(ruscorp$adult)

# code by target child 
ruscorp$targetchild <- NA
ruscorp$targetchild[ grep("^A",ruscorp$ref,perl=TRUE) ] <- "ALJ"
ruscorp$targetchild[ grep("^J",ruscorp$ref,perl=TRUE) ] <- "JAS"
ruscorp$targetchild[ grep("^P",ruscorp$ref,perl=TRUE) ] <- "PAS"
ruscorp$targetchild[ grep("^V",ruscorp$ref,perl=TRUE) ] <- "VAN"
ruscorp$targetchild <- as.factor(ruscorp$targetchild)

# code age (from ref) so that adult data also contains the corresponding child age
ruscorp$childage <- NA
ruscorp$childage <- sub("^[A-Z][0-9]{3}([0-9]{5}).+","\\1",ruscorp$ref,perl=TRUE) 
ruscorp$childage <- as.numeric(ruscorp$childage)

# save(ruscorp,file="ruscorp.Rdata")


# Select verbs and add verb classes
#############
ruscorp.verbs <- ruscorp[grep("&GL",ruscorp$mor,perl=TRUE),]

# split glosses into transcribed verb and gloss
ruscorp.verbs$word <- sub("(^[^&]+).+","\\1",ruscorp.verbs$mor,perl=TRUE)
ruscorp.verbs$gloss <- sub("^[^&]+&GL-([^:]+.+)","\\1",ruscorp.verbs$mor,perl=TRUE)

# read in dictionary
dict <- read.delim("~/Documents/Research/language_acquisition/RussischCorpus/dict_import.txt")
dict$class <- as.factor(dict$class)

# merge on word
ruscorp.classes <- merge(ruscorp.verbs,dict,by="word")
ruscorp.classes$verbclass <- paste(ruscorp.classes$gloss, ruscorp.classes$class, sep="-")
# save(ruscorp.classes,file="ruscorp.classes.Rdata")


# Entropy computations
########################
entr.ML <- function(x) {
	counts <- as.data.frame(xtabs(~x))$Freq
	counts <- counts[counts>0] #remove forms that don't actually belong to the frequency table but are produced by xtabs()
	return(entropy(counts, method='ML', unit="log2"))
}
ruscorp.entropies <- aggregate(list(H=ruscorp.classes$verbclass),  list(targetchild=ruscorp.classes$targetchild, adult=ruscorp.classes$adult, childage=ruscorp.classes$childage), entr.ML)
# save(ruscorp.entropies,file="ruscorp.entropies.Rdata")


# Noun/verb ratio computations
##############################
nvr.form.tokens <- function(x) {x <- x[!is.na(x)]
	length(x[grep("&SUW", x)])/(length(x[grep("&SUW", x)])+length(x[grep("&GL",x)]))
}
nvr.types <- function(x) {
	length(unique(x[grep("&SUW", x)]))/(length(unique(x[grep("&SUW",x)]))+length(unique(x[grep("&GL",x)])))
}
ruscorp.nvr <- summaryBy(mor~targetchild+adult+childage, data=ruscorp, FUN=function(x) c(tokens=nvr.form.tokens(x), types=nvr.types(x)))