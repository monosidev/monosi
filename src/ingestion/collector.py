class Collector:
    def run(self):
        # Create Tasks
        tasks = self._create_tasks()

        # Run tasks
        for task in tasks:
            task_results_gen = task.run()
            while True:
                try:
                    units_results_gen = next(task_results_gen)
                    
                    while True:
                        try:
                            unit_results = next(units_results_gen)
                            self.push(unit_results)
                        except StopIteration:
                            break
                except StopIteration:
                    break


