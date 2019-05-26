from genome import Genome
from species import Species


class Population:
    def __init__(self, size):
        self.pop = []
        self.best_score = 0
        self.gen = 0
        self.innovation_history = []
        self.species = []

        self.mass_extinction_event = False
        self.new_stage = False
        self.population_life = 0

        for i in range(size):
            self.pop.append(Genome())
            self.pop[i].generate_network()
            self.pop[i].mutate(self.innovation_history)

    def update_alive(self):
        self.population_life += 1
        for i in range(len(self.pop)):
            if not self.pop[i].dead:
                self.pop[i].look()
                self.pop[i].think()
                self.pop[i].update()

    def done(self):
        for i in range(len(self.pop)):
            if not self.pop[i].dead:
                return False
        return True

    def set_best_genome(self):
        temp_best = self.species[0].genomes[0]
        temp_best.gen = self.gen

        if temp_best.score > self.best_score:
            self.best_score = temp_best.score

    def natural_selection(self):
        self.speciate()
        self.calculate_fitness()
        self.sort_species()
        if self.mass_extinction_event:
            self.mass_extinction()
            self.mass_extinction_event = False
        self.cull_species()
        self.set_best_genome()
        self.kill_stale_species()
        self.kill_bad_species()

        average_sum = self.get_avg_fitness_sum()
        children = []
        for j in range(len(self.species)):
            children.append(self.species[j].champ.clone())
            no_of_children = int(self.species[j].average_fitness / average_sum * len(self.pop)) - 1
            for i in range(no_of_children):
                children.append(self.species[j].give_me_baby(self.innovation_history))

        while len(children) < len(self.pop):
            children.append(self.species[0].give_me_baby(self.innovation_history))
        self.pop = children
        self.gen += 1
        for i in range(len(self.pop)):
            self.pop[i].generate_network()
        self.population_life = 0

    def speciate(self):
        for s in self.species:
            s.genomes.clear()
        for i in range(len(self.pop)):
            species_found = False
            for s in self.species:
                if s.same_species(self.pop[i]):
                    s.add_to_species(self.pop[i])
                    species_found = True
                    break
            if not species_found:
                self.species.append(Species(self.pop[i]))

    def calculate_fitness(self):
        for i in range(len(self.pop)):
            self.pop[i].calculate_fitness()

    def sort_species(self):
        for s in self.species:
            s.sort_species()

        temp = []
        for _ in range(len(self.species)):
            mx = 0
            max_index = 0
            for i in range(len(self.species)):
                if self.species[i].best_fitness > mx:
                    mx = self.species[i].best_fitness
                    max_index = i
            temp.append(self.species[max_index])
            del self.species[max_index]
        self.species = temp

    def kill_stale_species(self):
        i = 2
        while i < len(self.species):
            if self.species[i].staleness >= 15:
                del self.species[i]
            else:
                i += 1

    def kill_bad_species(self):
        average_sum = self.get_avg_fitness_sum()

        i = 2
        while i < len(self.species):
            if self.species[i].average_fitness / average_sum * len(self.pop) < 1:
                del self.species[i]
            else:
                i += 1

    def get_avg_fitness_sum(self):
        average_sum = 0
        for s in self.species:
            average_sum += s.average_fitness
        return average_sum

    def cull_species(self):
        for s in self.species:
            s.cull()
            s.fitness_sharing()
            s.set_average()

    def mass_extinction(self):
        self.species = self.species[:5]
