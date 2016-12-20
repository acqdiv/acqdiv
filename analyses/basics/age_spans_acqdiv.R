library(dplyr)
library(ggplot2)
library(grid)


load('../../database/acqdiv_corpus_2016-09-22.rda')


common_theme <- 
  # black and white theme 
  theme_bw() +
  # common font size
  # theme(text = element_text(family = 'CMU Sans Serif', size=12))
  theme(text = element_text(family = 'Linux Libertine O', size=12),
  axis.text = element_text(size=12),
  axis.title.y = element_text(vjust=0.9),
  legend.text=element_text(size=11),
  strip.text = element_text(size=12)
  )


# colorblind-friendly palette from
# http://jfly.iam.u-tokyo.ac.jp/color/
# substitutes black with gray
# cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
# darkPalette <- c("#377eb8", "#ff7f00", "#e6ab02", "#4daf4a", "#e41a1c", "#984ea3", "#D55E00")
# scale_colour_discrete <- function(...) scale_colour_manual(values=darkPalette, ...)
# scale_fill_discrete <- function(...) scale_fill_manual(values=darkPalette, ...)


theme_set(common_theme)


# --- age breaks/labels
age.breaks <- c(6*30.4, 12*30.4, 18*30.4, 24*30.4, 30*30.4, 
				36*30.4, 42*30.4, 48*30.4, 54*30.4, 60*30.4,
				66*30.4, 72*30.4, 78*30.4, 84*30.4, 90*30.4, 
				96*30.4, 102*30.4, 108*30.4)
age.labels <- c("0;6", "1;0", "1;6", "2;0", "2;6", 
				"3;0", "3;6", "4;0", "4;6", "5;0", 
				"5;6", "6;0", "6;6", "7;0", "7;6",
				"8;0", "8;6", "9;0")


# plot showing age range of target children
target_children_ages <- speakers %>%
	filter(!is.na(age_in_days)) %>% 
	select(age_in_days, macrorole, speaker_id, language, corpus, speaker_label, name) %>%
	mutate(speaker_id2=paste(speaker_label, name, sep='_')) %>%
	filter(grepl('Target_Child', macrorole)) %>%
	group_by(corpus, speaker_id2) %>%
	summarize(youngest.at = min(age_in_days),
		 		oldest.at = max(age_in_days)) %>%
	select(corpus, speaker_id2, age=youngest.at, oldest.at) %>% as.data.frame

# ok, this is lame, but whatever, not in the mood to thing harder
target_children_ages2 <- target_children_ages %>% 
		select(corpus, speaker_id2, age=oldest.at) %>% 
		as.data.frame
target_children_ages <- rbind(target_children_ages[,c('corpus', 'speaker_id2', 'age')], target_children_ages2)



target_children_ages <- target_children_ages %>% 
	# filter(!(corpus %in% c('Cree', 'Indonesian'))) %>%
	mutate(Corpus=corpus, 
		Age=age)


# add order number to have ... err yeah, order:
target_children_ages$order <- rep(1:45,2)
## target_children_ages$order <- rep(1:35,2)


ggplot(target_children_ages, aes(x=Age, y=1, color=Corpus)) + 
	geom_point(size=.8) + 
	geom_line(size=1.5) + 
	# cheat and do facets :)
	facet_wrap(~order, ncol=1) + 
	# remove axis ticks and labels on y axis
	theme(axis.ticks.y = element_blank(), axis.text.y = element_blank(),
		# remove spaces between facets
		panel.margin=unit(-.6, "lines"), 
		# it’s irrelevant which child is which line, so remove facet titles:
		strip.background = element_blank(), 
		strip.text = element_blank(),
		# optional: remove panel outlines:
		panel.border = element_blank()) +
	labs(y="")  +
	scale_x_continuous(breaks=age.breaks,
						labels=age.labels) +
	guides(fill=guide_legend(title=""))
