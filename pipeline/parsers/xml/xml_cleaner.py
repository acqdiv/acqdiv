import copy
import itertools
import json
import logging
import os
import pdb
import re
import sys

from collections import defaultdict
from lxml import etree

from pipeline.parsers.metadata import Chat


class XMLCleaner(object):
    """
    This class transforms the XML output of Chatter into a mostly clean XML
    format that the XML Parser can parse into the appropriate data structures
    for the Processor. It provides methods usable for cleaning most parts of
    most corpora, with the exception of morphology, which is handled
    differently by each corpus and thus must be implemented by a per-corpus
    cleaner class.
    """

    logger = logging.getLogger('pipeline.' + __name__)

    @staticmethod
    def creadd(location, key, value):
        """
        Method to add a string value to a dictionary where a value may
        already be present. If so, the values are concatenated by '; '.

        Args:
        location: the dictionary to add to
        key: the dictionary key
        value: the value to add

        Returns:
        None
        """
        if key not in location.keys() or location[key] is None:
            location[key] = value
        else:
            if value in location[key]:
                pass
            else:
                location[key] += '; ' + value

    @staticmethod
    def word_index_up(ls, llen, idx, parent):
        """
        Method to add a new word to an XML Utterance node that is also
        tracked by a list. This is a common occurrence in the restructuring
        workflow. Primarily used internally by corpus-specific subclasses for
        dealing with misalignments between words and morphemes.

        Args:
        ls: the list of words to add to
        llen: the list's length
        idx: the index in ls of the position to insert after
        parent: the parent node of the new word

        Returns:
        the new index and length of the list
        """
        idx += 1
        if idx >= llen:
            new_word = etree.Element('w')
            act = etree.SubElement(new_word, 'actual')
            tar = etree.SubElement(new_word, 'target')
            act.text = '???'
            tar.text = '???'
            new_word.attrib['dummy'] = 'misaligned morphemes'
            parent.insert(llen, new_word)
            ls.insert(llen, new_word)
            llen += 1
        return idx, llen

    @staticmethod
    def find_text(parent, child):
        """
        Convenience method to get the text of a node that may be None.

        Args:
        parent: Node to search in
        child: Node to search for

        Returns:
        the text of the child node if it was found, None otherwise
        """
        se = parent.find(child)
        return se.text if se is not None else None

    @staticmethod
    def find_xpath(parent, xpexpr):
        """
        Convenience method to find the first node matching an XPath
        expression if any.

        Args:
        parent: the node to search in
        xpexpr: the XPath expression to use

        Returns:

        """
        ses = parent.xpath(xpexpr)
        return ses[0] if len(ses) != 0 else None

    def __init__(self, cfg, fpath):
        self.cfg = cfg
        self.fpath = fpath
        self.sname = os.path.basename(fpath).split('.')[0]
        #self.metadata_parser = Chat(cfg, fpath)

    def _clean_xml(self):
        """
        Main method of the XML Cleaner. Parses the XML file to be cleaned
        using LXML, strips out namespaces, then loops through the utterances
        and calls the cleaning methods on them. If there is an otherwise
        unhandled exception during the cleaning workflow, that utterance
        is removed from the final XML Document.

        Args: self

        Returns: The cleaned XML tree
        """

        xmldoc = etree.parse(self.fpath)
        root = xmldoc.getroot()

        for elem in root.iter():
            # remove prefixed namespaces
            try:
                elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
                tag = elem.tag
                attrib = elem.attrib
            except TypeError:
                pass

        for u in xmldoc.iterfind('.//u'):

            try:
                self._clean_xml_utterance(u)
            except Exception as e:
                XMLCleaner.logger.warning("Aborted processing of utterance {} "
                        "in file {} with error: {}".format(
                            u.attrib.get('uID'), self.fpath, repr(e)),
                                          exc_info=sys.exc_info())
                u.getparent().remove(u)

        return xmldoc

    def _debug_xml(self, fd):
        """
        Method to write the cleaned XML Tree to a file. Not used in the acqdiv
        pipeline at the moment, but could theoretically be used to automatically
        create pretty versions of XML corpora.

        Args:
          fd: A file-like object to write to
        """
        xmld = self._clean_xml()
        fd.write(etree.tostring(xmld, encoding='unicode',
                                        pretty_print=True))

    def _clean_xml_utterance(self, u):
        """
        Method that calls the various cleaning methods on a specific
        utterance.

        Args:
          u: A <u> tag in the XML tree.
        """

        if self.cfg['morphemes']['repetitions_glossed'] == 'yes':
            self._word_inference(u)
            self._clean_groups(u)
            self._process_morphology(u)
        else:
            self._word_inference(u)
            self._process_morphology(u)
            self._clean_groups(u)
        self._morphology_inference(u)
        self._add_morphology_warnings(u)
        self._set_morpheme_language(u)
        self._restructure_metadata(u)
        self._remove_junk(u)

    def _word_inference(self, u):
        """
        Handles special ChatXML constructs in words, lifting them to the
        main text/morpheme level. The modifications are done in-place,
        with no return value.

        Args:
          u: A <u> tag in the XML tree.
        """
        words = u.findall('.//w')
        self._restructure_words(words)
        self._clean_word_text(words)
        self._clean_fragments_and_omissions(words)
        self._clean_shortenings(words)
        self._clean_replacements(words)
        self._mark_retracings(u)
        self._add_word_warnings(words)

    @staticmethod
    def _restructure_words(words):
        """
        Extracts the main text of a word from around any intervening tags and
        creates the actual and target subtags. The text is stored in <actual>.

        Args:
          words: A list of <w> tags in the XML tree.
        """
        for w in words:
            if w.text is not None:
                wt = w.text
            else:
                wt = ''.join(e.tail if e.tail is not None else '' for e in w)
            actual = etree.SubElement(w, 'actual')
            target = etree.SubElement(w, 'target')
            actual.text = wt
            target.text = ''
            w.text = ''

    @staticmethod
    def _clean_word_text(words):
        """
        Extracts text from special form tags and adds it to the text
        of their parent tags.

        Args:
          words: A list of <w> tags in the XML tree.
        """
        for w in words:
            wt = w.find('actual')
            #TODO: what with p in replacements etc. ?
            for path in ('.//p', './/ca-element', './/wk'):
                for t in w.findall(path):
                    parent = t.getparent()
                    if t.tail is not None:
                        if parent == w:
                            if wt.text is None:
                                wt.text = t.tail
                            else:
                                wt.text += t.tail
                        else:
                            if parent.text is None:
                                parent.text = t.tail
                            else:
                                parent.text += t.tail
                    parent.remove(t)
            if wt.text:
                # Sometimes words may be partially untranscribed
                # (-xxx, xxx-, -xxx-) - transform this to unified ???
                wt.text = re.sub('\-?xxx\-?', '???', wt.text)
            if 'untranscribed' in w.attrib:
                wt.text = '???'

    @staticmethod
    def _clean_fragments_and_omissions(words):
        """
        Deals with words tagged as "fragment" or "omission".
        Fragments have no text and aren't glossed, while
        omissions are simply empty entirely.

        Args:
          words: A list of <w> tags in the XML tree.
        """
        for w in words:
            if 'type' in w.attrib:
                if w.attrib['type'] == 'omission':
                    w = None
                elif w.attrib['type'] == 'fragment':
                    w.find('target').text = '???'
                    w.attrib['warning'] = 'not glossed'

    @staticmethod
    def _clean_shortenings(words):
        """
        Deals with shortenings. Shortenings enclose omitted text which
        is added to the target text.

        Args:
          words: A list of <w> tags in the XML tree.
        """
        for w in words:

            w_actual = w.find('actual')
            w_target = w.find('target')
            w_target.text = w_actual.text

            for s in w.findall('shortening'):
                if s.text is not None:
                    w_target.text += s.text
                if s.tail is not None:
                    w_target.text += s.tail
                    w_actual.text += s.tail
                w.remove(s)

    def _set_morpheme_language(self, u):
        """
        Sets the morpheme language for an utterance. The morpheme language is set
        on a by-word basis, since the indicating tags, if present, are children
        of <w>. If no such tags are found, we instead use the default language
        of the corpus.

        Args:
          u: A <u> tag in the XML tree.
        """
        if self.cfg['morphemes']['language'] == 'yes':
            for fw in u.iterfind('.//w'):
                l = fw.find('langs')
                if l is not None:
                    ltext = self.cfg['languages'][l[0].text]
                    fw.remove(l)
                else:
                    ltext = self.cfg['corpus']['language']
                nl = etree.SubElement(fw, 'language')
                nl.text = ltext
                for m in fw.iterfind('.//m'):
                    m.attrib['morpheme_language'] = ltext
        else:
            for fw in u.iterfind('.//w'):
                for m in fw.iterfind('.//m'):
                    m.attrib['morpheme_language'] = self.cfg['corpus']['language']

    @staticmethod
    def _clean_replacements(words):
        """
        Cleans replacements, e.g.
        <g><w>burred<replacement><w>word</w></replacement></w></g>.
        Replacement words may contain shortenings, but these don't have
        to be specially dealt with because _clean_shortenings operates on
        <w> nested at arbitrary depth in the utterance.

        The replacement structure is transformed into an appropriate difference
        between actual and target text in the final XML tree. Since replacement
        targets and actuals may contain differing numbers of words, new <w>
        elements are inserted where appropriate.

        Args:
          words: A list of <w> elements in the XML tree.
        """
        for fw in words:
            r = fw.find('replacement')
            if r is not None:
                rep_words = r.findall('w')
                rep_len = len(rep_words)
                wp = fw.getparent()
                i = wp.index(fw)

                # go through words in replacement
                for j in range(rep_len):
                    # check for morphology
                    mor = rep_words[j].find('mor')
                    # first word: transfer content
                    # and any morphology to parent <w> in <u>
                    if j == 0:
                        fw.find('target').text = rep_words[0].find('target').text
                        if mor is not None:
                            fw.append(mor)
                    # all further words: insert new empty <w> under parent of
                    # last known <w> (= <u> or <g>),
                    # put content and morphology there
                    else:
                        w = etree.Element('w')
                        w_act = etree.SubElement(w, 'actual')
                        w_tar = etree.SubElement(w, 'target')
                        w_tar.text = rep_words[j].find('target').text
                        if mor is not None:
                            w.append(mor)
                        wp.insert(i+j, w)

                #fw.attrib['target'] = '_'.join(rep_w.attrib['target'] 
                #        for rep_w in r.findall('w'))
                fw.remove(r)

    @staticmethod
    def _mark_retracings(u):
        """
        This tags words in retracings with glossed=ahead, which is required
        by the retracing cleaning code.

        Args:
          u: A <u> element in the XML tree.
        """
        for group in u.iterfind('.//g'):
            retracings = group.find('k[@type="retracing"]')
            retracings_wc = group.find('k[@type="retracing with correction"]')
            if (retracings is not None) or (retracings_wc is not None):
                words = group.findall('.//w')
                for w in words:
                    w.attrib['glossed'] = 'ahead'
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed; search ahead')

    @staticmethod
    def _add_word_warnings(words):
        """
        Adds warnings about irregular glossing/transcription to the "warning"
        attribute of <w> elements.

        Args:
          words: A list of words.
        """
        for w in words:
            if 'glossed' in w.attrib:
                if w.attrib['glossed'] == 'no':
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed')
                elif w.attrib['glossed'] == 'repeated':
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed; repeat')
                elif w.attrib['glossed'] == 'ahead':
                    XMLCleaner.creadd(w.attrib, 'warning', 'not glossed; search ahead')
            if 'transcribed' in w.attrib and w.attrib['transcribed'] == 'insecure':
                XMLCleaner.creadd(w.attrib, 'warning', 'transcription insecure')

    @staticmethod
    def _clean_groups(u):
        """
        Cleans up <g> elements, which wrap the following special forms:
        Repetitions, retracings and guesses. <g> groups may be nested at
        arbitrary depth, and occur in the corpus nested to at least three
        levels, so this function recursively cleans them bottom-up.

        Args:
          u: A <u> element in the XML tree.
        """
        for group in u.iterfind('g'):

            subgroups = group.findall('g')
            if subgroups != []:
                for subgroup in subgroups:
                    self._clean_groups(subgroup)

            parent = group.getparent()
            idx = parent.index(group)

            XMLCleaner._clean_repetitions(group)
            XMLCleaner._clean_retracings(group, u)
            XMLCleaner._clean_guesses(group)
            for w in group.iterfind('.//w'):
                parent.insert(idx, w)
                idx += 1
            parent.remove(group)

    @staticmethod
    def _clean_repetitions(group):
        """
        Cleans repetitions. Repetitions are a special form that marks
        that the words within it are repeated. We replace this special form
        by simple duplication of the words in the final XML tree.

        Args:
          group: A <g> element.
        """
        reps = group.find('r')
        if reps is not None:
            ws = group.findall('.//w')
            idx = group.index(ws[-1])
            for i in range(int(reps.attrib['times'])-1):
                for w in ws:
                    group.insert(idx+1, copy.deepcopy(w))
                    idx += 1

    @staticmethod
    def _clean_retracings(group, u):
        """
        Cleans retracings. This involves a lot of searching for morphology and
        then copying it to retraced words. Retracings with and without
        corrections must be treated differently from each other, because
        in the second case, we cannot match on the word text to find out which
        elements correspond to each other.

        Args:
          group: A <g> element.
          u: The utterance element that is the ultimate parent of group.
        """
        retracings = group.find('k[@type="retracing"]')
        retracings_wc = group.find('k[@type="retracing with correction"]')

        if retracings is not None:
            group_ws = group.findall('w')
            for w in group_ws:
                elems_with_same_text = [e for e in u.iterfind('.//w')
                        if e.find('actual').text == w.find('actual').text]
                for elem in elems_with_same_text:
                    mor = elem.find('mor')
                    # if there is <mor>, insert below the retraced word
                    if mor is not None:
                        w.append(copy.deepcopy(mor))
                        if 'warning' in w.attrib:
                            w.attrib['warning'] = re.sub(
                                'not glossed; search ahead',
                                    '', w.attrib['warning'])
                            if w.attrib['warning'] == '':
                                del w.attrib['warning']
                        w.find('target').text = elem.find('target').text
                        break
                if w.find('mor') is None:
                    if 'warning' in w.attrib:
                        w.attrib['warning'] = re.sub('; search ahead',
                                '', w.attrib['warning'])
                if 'glossed' in w.attrib:
                    del w.attrib['glossed']

        elif retracings_wc is not None:
            group_ws = group.findall('w')
            u_ws = u.findall('.//w')
            base_index = u_ws.index(group_ws[-1]) + 1
            max_index = base_index + len(group_ws)
            for i,j in zip(range(base_index, max_index), itertools.count()):
                try:
                    mor = u_ws[i].find('mor')
                    if mor is not None:
                        group_ws[j].append(copy.deepcopy(mor))
                        if 'warning' in group_ws[j].attrib:
                            re.sub('not glossed; search ahead', '',
                                    group_ws[j].attrib['warning'])
                    else:
                        if 'warning' in group_ws[j].attrib:
                            re.sub('; search ahead', '',
                                group_ws[j].attrib['warning'])
                    group_ws[j].find('target').text = u_ws[i].find('target').text
                except IndexError:
                    if 'warning' in group_ws[j].attrib:
                        re.sub('; search ahead', '',
                            group_ws[j].attrib['warning'])
                if 'glossed' in group_ws[j].attrib:
                    del group_ws[j].attrib['glossed']

    @staticmethod
    def _clean_guesses(group):
        """
        Cleans guesses.

        Args:
          group: A <g> element of the XML tree.
        """
        words = group.findall('.//w')
        target_guess = group.find('.//ga[@type="alternative"]')
        if target_guess is not None:
            words[0].find('target').text = target_guess.text

        guesses = group.find('k[@type="best guess"]')
        if guesses is not None:
            for w in words:
                w.attrib['transcribed'] = 'insecure'

    def _process_morphology(self, u):
        """
        Morphology is handled completely differently by each corpus,
        so we do not provide a default implementation. This method
        must be overridden by each corpus-specific cleaner.
        """
        pass

    def _morphology_inference(self, u):
        """
        Morphology is handled completely differently by each corpus,
        so we do not provide a default implementation. This method
        must be overridden by each corpus-specific cleaner.
        """
        pass

    @staticmethod
    def _add_morphology_warnings(u):
        """
        Adds warnings about broken alignment to the morphology tiers.

        Args:
          u: A <u> element of the XML tree.
        """
        if u.find('.//mor') is None:
            XMLCleaner.creadd(u.attrib, 'warning', 'not glossed')
        else:
            for w in u.findall('.//w'):
                if w.find('./mor') is None:
                    XMLCleaner.creadd(u.attrib, 'warning',
                                      'broken alignment full_word : '
                                      'segments/glosses')
                    break

    def _restructure_metadata(self, u):
        """
        Converts metadata forms of the type
        <a type="xxx"/> into differentiated tags of the form <xxx/>.
        Also performs tier renaming using the corpus .ini so that
        the XML Parser can access a unified list of metadata tags.

        Args:
          u: A <u> element of the XML tree.
        """
        for a in u.findall('a'):
            if a.attrib['type'] == 'extension':
                ntag = a.attrib['flavor']
                del a.attrib['flavor']
            else:
                ntag = a.attrib['type']
                if ' ' in ntag:
                    ntag = ntag.replace(' ', '_')
            a.tag = self.cfg['xml_mappings'].get(ntag, ntag)
            del a.attrib['type']

        stype = u.find('t')
        if stype is not None:
            stype.attrib['type'] = self.cfg['correspondences'][
                stype.attrib.get('type')]

        timestamp = u.find('time') if u.find('time') is not None else u.find('time_stamp')
        if timestamp is not None:
            timestamp.attrib['start'] = timestamp.text
            timestamp.text = ''
            timestamp.tag = 'media'

    def _remove_junk(self, u):
        """
        This is a utility method that can be overridden by corpus-specific
        cleaners to remove any unused items in that corpus' XML utterances.
        """
        pass

    def clean(self):
        """
        Public wrapper around _clean_xml.
        """
        return self._clean_xml()


if __name__ == '__main__':
    print("Sorry, there's nothing here!")
