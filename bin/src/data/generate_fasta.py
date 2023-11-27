import random
from abc import ABC
import numpy as np
import pyjaspar

class Fasta(ABC):
    """
    This class is the master class for all fasta related classes.
    """

    # init function for the fasta class, takes as input the path to the fasta file
    def __init__(self):
        self.sequences = []
        self.sequence_names = []
        self.tags = []

    def write_fasta(self, path_to_write):
        """
        This function is a helper function for writing a fasta file taking as input self. 
        Fasta should be the following format : 
        
        >sequence_name|tag
        sequence

        Self has to contain sequences, tags and names. 
        """
        
        # check if sequences, sequences_names and tags are populated; if an error is thrown, print the length of each list
        assert len(self.sequences) == len(self.sequence_names) == len(self.tags), f"The sequences, sequence_names and tags lists should have the same length. The sequences list is of length {len(self.sequences)}, the sequence_names list is of length {len(self.sequence_names)} and the tags list is of length {len(self.tags)}"
        # check if there is at least one sequence
        assert len(self.sequences) > 0, "There should be at least one sequence"

        with open(path_to_write, 'w') as fasta_file:
            for sequence, sequence_name, tag in zip(self.sequences, self.sequence_names, self.tags):
                fasta_file.write(f">{sequence_name}|{tag}\n")
                fasta_file.write(sequence + '\n')

    def write_fasta_without_tags(self, path_to_write):
        """
        This function is a helper function for writing a fasta file taking as input self. 
        Fasta should be the following format : 
        
        >sequence_name
        sequence

        Self has to contain sequences and names. 
        """
        
        # check if sequences and sequences_names are populated; if an error is thrown, print the length of each list
        assert len(self.sequences) == len(self.sequence_names), f"The sequences and sequence_names lists should have the same length. The sequences list is of length {len(self.sequences)} and the sequence_names list is of length {len(self.sequence_names)}"
        # check if there is at least one sequence
        assert len(self.sequences) > 0, "There should be at least one sequence"

        with open(path_to_write, 'w') as fasta_file:
            for sequence, sequence_name in zip(self.sequences, self.sequence_names):
                fasta_file.write(f">{sequence_name}\n")
                fasta_file.write(sequence + '\n')

    def load_fasta(self, path_to_read):
        """
        This function is a helper function for loading a fasta file taking as input self. 
        Fasta should be the following format : 
        
        >sequence_name|tag
        sequence

        Self has to contain sequences, tags and names. 
        """
        with open(path_to_read, 'r') as fasta_file:
            for line in fasta_file:
                if line[0] == '>':
                    # this is a sequence name
                    sequence_name, tag = line[1:].split('|')
                    self.sequence_names.append(sequence_name)
                    # convert tag to float
                    self.tags.append(float(tag.strip()))
                else:
                    # this is a sequence
                    # check if the sequence contains 'n' or 'N' and if so, remove the previously added tag and sequence names
                    if 'n' in line or 'N' in line:
                        self.sequence_names.pop()
                        self.tags.pop()        
                    else:                      
                        self.sequences.append(line.strip())

    def load_fasta_without_tags(self, path_to_read):
        """
        This function is a helper function for loading a fasta file taking as input self. 
        Fasta should be the following format : 
        
        >sequence_name
        sequence

        Self has to contain sequences and names. 
        """
        with open(path_to_read, 'r') as fasta_file:
            for line in fasta_file:
                if line[0] == '>':
                    # this is a sequence name
                    sequence_name = line[1:].strip()
                    self.sequence_names.append(sequence_name)
                else:
                    # this is a sequence

                    # check if the sequence contains 'n' or 'N' and if so, remove the previously added sequence name
                    if 'n' in line or 'N' in line:
                        self.sequence_names.pop()                   
                    else:                     
                        self.sequences.append(line.strip())

    def get_sequence_length(self):
        """ This function returns the length of the sequences in the fasta file. """
        return len(self.sequences[0])

class GenerateFasta(Fasta):
    """
    This class heritates from the fasta class and is used as a master class to generate dummy fasta files.
    """
    
    def __init__(self, dna_sequence_length):
        super().__init__()
        self.dna_sequence_length = dna_sequence_length

    def generate_random_dna_sequence(self):
        """ Generate a random DNA sequence, with length self.dna_sequence_length."""
        dna_sequence = ''.join(random.choice('ACGT') for _ in range(self.dna_sequence_length))
        return dna_sequence

    def generate_motif_from_pwm(self, pwm):
        """ Generate a motif from a pwm. """
        motif = ''
        for i in range(pwm.shape[1]):
            motif += np.random.choice(['A', 'C', 'G', 'T'], p=pwm[:, i])
        return motif

    def assess_match_between_motif_and_pwm(self, motif, pwm):
        """ assesses the match between a motif and a pwm of the same length. This returns the max PWM score if it is a perfect match and the min PWM score if it is the worst match. 
        The PWM should be a numpy array describing the probability of finding a nucleotide at a given position.
        The motif should be a string of nucleotides. 
        The PWM should be of shape (4, motif_length) with the nucleotides probabilities in this order : A,C,G,T."""

        assert len(motif) == pwm.shape[1], "The motif and the PWM should have the same length"
        motif_score = 0
        for i, nucleotide in enumerate(motif):
            if nucleotide == 'A':
                motif_score += pwm[0, i]
            elif nucleotide == 'C':
                motif_score += pwm[1, i]
            elif nucleotide == 'G':
                motif_score += pwm[2, i]
            elif nucleotide == 'T':
                motif_score += pwm[3, i]
        return motif_score

    def insert_motif_in_sequence(self, sequence, motif, start=None):
        """ This static method takes a sequence and a motif as input and incorporates the motif in the said sequence.
        If the start parameter is set to None, the motif starting input position is chosen randomly. 
        If the start parameter is set to an integer, the motif starting input position is the said integer. 
        Note : the user is responsible for inputing an integer, and for making sure that the motif is not out of bounds. (f.e. start = 49 for a motif of length 10 in a sequence of length 50)"""
        if start is None:
            start = random.randint(0, len(sequence) - len(motif))
        sequence = sequence[:start] + motif + sequence[start + len(motif):]
        return sequence
    
    def get_motif_from_jaspar(self, motif_id):
        """ This function returns a motif from the jaspar database. """
        jaspar_db = pyjaspar.jaspardb()
        motif = jaspar_db.fetch_motif_by_id(motif_id)
        # convert the motif pwm to a numpy array
        # start by unrolling the dictionary contained in the motif.pwm attribute
        unrolled = [np.array(motif.pwm[key]) for key in motif.pwm.keys()]
        # stack the arrays
        pwm = np.stack(unrolled)
        return pwm
    

class GenerateSingleFixedMotifDataset(GenerateFasta):
    """ This class generates a simple balanced dataset with a single fixed motif being present in some sequences. Said sequences are associated a positive label where the non motif sequences are associated a negative label. """
    
    def __init__(self, dna_sequence_length, motif, motif_tag, non_motif_tag, number_of_sequences=1000, motif_start=None):
        super().__init__(dna_sequence_length)
        self.motif = motif
        self.motif_start = motif_start
        self.motif_tag = motif_tag
        self.non_motif_tag = non_motif_tag
        self.number_of_sequences = number_of_sequences
        self.generate_dataset()

    def generate_dataset(self):
        """ This function generates the dataset. """
        for i in range(self.number_of_sequences):
            sequence = self.generate_random_dna_sequence()
            sequence = self.insert_motif_in_sequence(sequence, self.motif, self.motif_start)
            self.sequences.append(sequence)
            self.sequence_names.append(f"sequence_{i}")
            self.tags.append(self.motif_tag)
        for i in range(self.number_of_sequences):
            sequence = self.generate_random_dna_sequence()
            self.sequences.append(sequence)
            self.sequence_names.append(f"sequence_{i + self.number_of_sequences}")
            self.tags.append(self.non_motif_tag)

class GenerateSingleJasparMotifDataset(GenerateFasta):
    """ This class generate a Dataset with a single motif from the jaspar database. """
    
    def __init__(self, dna_sequence_length, jaspar_motif_id):
        super().__init__(dna_sequence_length)
        self.jaspar_motif = self.get_motif_from_jaspar(jaspar_motif_id)

    def generate_dataset(self, number_of_sequences, motif_start=None, path_fasta=None):
        # if the path to fasta is specified, load the fasta file
        if path_fasta:
            self.load_fasta(path_fasta)

            # check if the sequences are of the right length, throw an error if not since it is not going to fit the model, in the error message, also specify the length of the sequences in the fasta file and the user input
            assert len(self.sequences[0]) == self.dna_sequence_length, f"The sequences in the fasta file are of length {len(self.sequences[0])} while the user input dna_sequence_length is {self.dna_sequence_length}"

            # update the number_of_sequences variable
            number_of_sequences = len(self.sequences)

            # reset the tag list to empty for generation
            self.tags = []


        # otherwise generate number_of_sequences sequences randomly with their names
        else:
            for i in range(number_of_sequences):
                sequence = self.generate_random_dna_sequence()
                sequence_name = f"sequence_{i}"
                self.sequences.append(sequence)
                self.sequence_names.append(sequence_name)

        # Then for half of the sequences, generate a motif from the jaspar pwm, then assess the match between the generated motif and the pwm, insert the motif in the sequence and add the motif/pwm match score to the tags
        for i in range(number_of_sequences):
            if i < number_of_sequences / 2:
                # generate a motif from the jaspar pwm
                motif = self.generate_motif_from_pwm(self.jaspar_motif)
                # assess the match between the generated motif and the pwm
                motif_score = self.assess_match_between_motif_and_pwm(motif, self.jaspar_motif)
                # insert the motif in the sequence
                self.sequences[i] = self.insert_motif_in_sequence(self.sequences[i], motif, motif_start)
                # add the motif/pwm match score to the tags
                self.tags.append(motif_score)
            else:
                # add a 0 tag to the sequences that do not have a motif
                self.tags.append(0)
