from .base import BaseResource

class JobListResource(BaseResource)
    def _get_jobs(self):
        """Returns a dictionary for all jobs info.
        It's a blocking operation.
        """
        jobs = self.manager.get_jobs()
        return_json = []
        for job in jobs:
            return_json.append(self._build_job_dict(job))
        return {'jobs': return_json}

    def _build_job_dict(self, job):
        """Transforms apscheduler's job structure to a python dictionary.
        :param Job job: An apscheduler.job.Job instance.
        :return: dictionary for job info
        :rtype: dict
        """
        if job.next_run_time:
            next_run_time = job.next_run_time.isoformat()
        else:
            next_run_time = ''
        return_dict = {
            'job_id': job.id,
            'name': job.name,
            'next_run_time': next_run_time,
            'job_class_string': utils.get_job_name(job),
            'pub_args': utils.get_job_args(job)}

        return_dict.update(utils.get_cron_strings(job))
        return return_dict

    def get(self):
        return self._get_jobs()
