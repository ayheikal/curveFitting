

import random
import math
import numpy as np

class Curve():
    def __init__(self):
        self.numberOfGenes =0
        self.b=1
        self.T=0
        self.points=[]
        self.numberOfPop=0



    """ generate and return array of random population"""
    def generatePop(self , number_of_pop):
        pop = []
        while(number_of_pop > 0):
            chrmo=list(np.random.uniform(-10,10,self.numberOfGenes))
            pop.append(chrmo)
            number_of_pop -= 1
        return pop

    """***************************crossover***********************"""
    """ apply single point crossover on two individuals and return the new ones"""
    def crossover_single_point(self , list_of_two_Lists):
        first = list(list_of_two_Lists[0])
        second = list(list_of_two_Lists[1])
        prob_crossover=random.randint(1 , self.numberOfGenes-1)
        for i in range(prob_crossover):
            first[i],second[i]=second[i],first[i]
        return [first , second]

    """ apply two point crossover on two individuals and return the new ones"""
    def crossover_two_points(self , list_of_two_Lists):
        first = list(list_of_two_Lists[0])
        second = list(list_of_two_Lists[1])
        prob_cross_1=random.randint(1 , self.numberOfGenes-1)
        prob_cross_2=random.randint(1 , self.numberOfGenes-1)
        while(prob_cross_1==prob_cross_2):
            prob_cross_1 = random.randint(1, self.numberOfGenes - 1)
            prob_cross_2 = random.randint(1, self.numberOfGenes - 1)
        if(prob_cross_1>prob_cross_2):
            prob_cross_1,prob_cross_2=prob_cross_2,prob_cross_1

        for i in range(prob_cross_1,prob_cross_2):
            first[i], second[i] = second[i], first[i]
        return [first , second]

    """apply uniform points on two individuals and return the new ones"""
    def crossoverbyUnifrom(self , list_of_two_Lists):
        first = list(list_of_two_Lists[0])
        second = list(list_of_two_Lists[1])
        itemsNumber = self.numberOfGenes
        for i in range(itemsNumber):
            probOfSwapGene = random.random()
            if(probOfSwapGene < 0.3):
                first[i], second[i] = second[i], first[i]

        return [first , second]

    """apply one technique of the crossover"""
    def crossoverFunc(self , list_of_two_lists):
        selectTechnique=random.random()
        if(selectTechnique<0.4): # single point
            return self.crossover_single_point(list_of_two_lists)
        elif(selectTechnique<0.7): # two points
            return self.crossover_two_points(list_of_two_lists)
        else:
            return self.crossoverbyUnifrom(list_of_two_lists)
       # else:
           # return list_of_two_lists

    """**************************mutation****************************"""
    """applay mutation function"""
    def mutationFunc(self , list_of_individuals,t,lowerBound=-10,upperBound=10):
        dl=du=0
        for chromosome in list_of_individuals:
            for index in range(len(chromosome)):
               # print('chromosome[index]: ',chromosome[index])
                r1 = random.random()
                #print('r1: ',r1)
                if (r1 < 0.8):
                    dl=chromosome[index]-lowerBound
                    du=upperBound-chromosome[index]
                    #print('dl: ',dl, "    du: ",du)

                    y=0
                    r2=random.random()
                    #print('r2: ',r2)
                    if(r2<=0.5):
                        y=dl
                    else:
                        y=du
                    r = random.random()
                    #print('r: ',r)
                    chromosome[index]=y*(1-(r**(1-((t/self.T)**self.b))))
                    #print('chrom: ',chromosome[index])
    """calculate cost error function"""

    def expectedValue(self,point,chromosome):
        sum=chromosome[0]
        for i in range(1,self.numberOfGenes):

            sum+=point[0]*pow(chromosome[i],i)
        return sum


# return (chromosome[0]+chromosome[1]*point[0]+chromosome[2]*(point[0]**2)+chromosome[3]*(pow(chromosome[3],3)))
    """return the evaluation fitness of a chromosome"""
    def estimateFitness(self,chromosome):
        n=len(self.points)
        sum=0
        mo=0
        for index in range(n):
            h=((self.expectedValue(self.points[index],chromosome)))
            y=((self.points[index][1]))
            mo=(h-y)
            c=mo**2
            sum+=c

        return sum/n #return inverse of mean square error to take max instead of min error

    """ return array of fitness for the all population"""
    def estimate_fitness_for_pop(self , pop):
        fitness = []
        for p in pop:
            fit = self.estimateFitness(p)
            fitness.append(fit)
        return fitness

    """select number of chromosomes using roulett wheele method"""
    def rolett_selection(self , numberofNewGeneration , pop , fitness):
        new_pop = []
        percentage = []
        fitness_sum = sum(fitness)
        previous = 0
        """ it must not enter this condition"""
        if(fitness_sum == 0):
            fitness_sum=0.00001

        for f in fitness:
            current = f/fitness_sum
            percentage.append(current + previous)
            previous += current

        for index in range(numberofNewGeneration):
            r = random.random()
            for i ,  per in enumerate(percentage):
                if r < per:
                    new_pop.append(pop[i])
                    break

        return new_pop

    """ generate new generation from the parents and the new offspring"""
    def apply_replacement(self ,pop_list , fitness_pop , offspring_list , fitness_offspring):
        half = int(len(pop_list)/2)

        # sort the parent population
        self.__bubbleSort(pop_list , fitness_pop)

        # sort the offspring population
        self.__bubbleSort(offspring_list , fitness_offspring)

        pop = pop_list[:half] + offspring_list[:half]

        return pop

    """sorting pop and their fitness depending on their fitness desc"""
    def __bubbleSort(self , arr , fit):
        n = len(fit)
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if fit[j] < fit[j + 1]:
                    fit[j], fit[j + 1] = fit[j + 1], fit[j]
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
    """estimate phenotype real value"""
    # def phenotypeValue(self,chrom):
    #     totalValue=0
    #     pairs=[]
    #     for index,value in enumerate(chrom):
    #         if(value==1):
    #             totalValue+=self.VALUE[index]
    #             pairs.append((self.WEIGHT[index],self.VALUE[index]))
    #
    #     return totalValue,pairs

    """general function to execute the algrithm"""
    def run(self , number_of_pop , number_of_trials):
        # init the population randomly
        self.numberOfPop=number_of_pop
        self.T=number_of_trials

        pop = self.generatePop(number_of_pop)
        fitness = self.estimate_fitness_for_pop(pop)
        print('pop' , pop)
        print('fit ' , fitness)
        # iterate n times to get the optimal solution
        for t in range(number_of_trials):
            # select the half of the population using roulett wheel
            selected_pop = self.rolett_selection(int(number_of_pop/2) , pop , fitness)
            length = len(selected_pop)
            # apply crossover from the selected_pop
            index = 0
            while index < length:
                #print(selected_pop[index], selected_pop[index+1])
                selected_pop += self.crossoverFunc([selected_pop[index], selected_pop[index+1]])
                index += 2

            # apply mutation over the selected_pop
            self.mutationFunc(selected_pop , t)

            # estimate the fitness for each individual in selected pop
            fitness_selected = self.estimate_fitness_for_pop(selected_pop)

            # apply replacement between parent and offspring
            pop=self.apply_replacement(pop , fitness , selected_pop , fitness_selected)
            fitness=self.estimate_fitness_for_pop(pop)
            #print('max: ',max(fitness))

        index_of_optimal = fitness.index(max(fitness))


        return pop[index_of_optimal]