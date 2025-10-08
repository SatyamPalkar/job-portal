import React, { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { applicationApi, jobApi, resumeApi } from '@/services/api';
import type { Application, Job, Resume } from '@/types';
import { ClipboardList, TrendingUp, Download, Mail } from 'lucide-react';

const Applications: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [jobs, setJobs] = useState<Record<number, Job>>({});
  const [resumes, setResumes] = useState<Record<number, Resume>>({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    setIsLoading(true);
    try {
      const appData = await applicationApi.getAll();
      setApplications(appData);

      // Fetch associated jobs and resumes
      const jobIds = [...new Set(appData.map(app => app.job_id))];
      const resumeIds = [...new Set(appData.map(app => app.resume_id))];

      const [jobsData, resumesData] = await Promise.all([
        Promise.all(jobIds.map(id => jobApi.getById(id).catch(() => null))),
        Promise.all(resumeIds.map(id => resumeApi.getById(id).catch(() => null))),
      ]);

      const jobsMap: Record<number, Job> = {};
      jobsData.filter(Boolean).forEach(job => {
        if (job) jobsMap[job.id] = job;
      });

      const resumesMap: Record<number, Resume> = {};
      resumesData.filter(Boolean).forEach(resume => {
        if (resume) resumesMap[resume.id] = resume;
      });

      setJobs(jobsMap);
      setResumes(resumesMap);
    } catch (error) {
      console.error('Error fetching applications:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateCoverLetter = async (applicationId: number) => {
    try {
      await applicationApi.generateCoverLetter(applicationId);
      await fetchApplications();
      alert('Cover letter generated successfully!');
    } catch (error) {
      console.error('Error generating cover letter:', error);
    }
  };

  const handleDownloadResume = async (applicationId: number, format: 'pdf' | 'docx' | 'txt') => {
    try {
      const response = await applicationApi.downloadResume(applicationId, format);
      alert(`Resume downloaded: ${response.file_path}`);
    } catch (error) {
      console.error('Error downloading resume:', error);
    }
  };

  const getMatchScoreColor = (score?: number) => {
    if (!score) return 'text-gray-600';
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'bg-gray-100 text-gray-700',
      submitted: 'bg-blue-100 text-blue-700',
      interviewing: 'bg-purple-100 text-purple-700',
      rejected: 'bg-red-100 text-red-700',
      accepted: 'bg-green-100 text-green-700',
    };
    return colors[status] || colors.draft;
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Applications</h1>
          <p className="mt-2 text-gray-600">
            Track your job applications and their status
          </p>
        </div>

        {isLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : applications.length === 0 ? (
          <Card>
            <div className="text-center py-12">
              <ClipboardList className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No applications yet</h3>
              <p className="text-gray-600 mb-4">
                Start applying to jobs with optimized resumes
              </p>
              <Button onClick={() => window.location.href = '/jobs'}>
                Browse Jobs
              </Button>
            </div>
          </Card>
        ) : (
          <div className="space-y-4">
            {applications.map((application) => {
              const job = jobs[application.job_id];
              const resume = resumes[application.resume_id];

              if (!job || !resume) return null;

              return (
                <div
                  key={application.id}
                  className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-xl font-semibold text-gray-900">
                          {job.title}
                        </h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(application.status)}`}>
                          {application.status}
                        </span>
                      </div>
                      <p className="text-gray-600">{job.company} - {job.location}</p>
                    </div>

                    {application.match_score !== undefined && (
                      <div className="text-right">
                        <div className="flex items-center">
                          <TrendingUp className={`h-5 w-5 mr-1 ${getMatchScoreColor(application.match_score)}`} />
                          <span className={`text-2xl font-bold ${getMatchScoreColor(application.match_score)}`}>
                            {Math.round(application.match_score)}%
                          </span>
                        </div>
                        <p className="text-sm text-gray-500">Match Score</p>
                      </div>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-500">Resume Used</p>
                      <p className="font-medium text-gray-900">{resume.title}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Applied Date</p>
                      <p className="font-medium text-gray-900">
                        {application.applied_at 
                          ? new Date(application.applied_at).toLocaleDateString()
                          : 'Not submitted yet'}
                      </p>
                    </div>
                  </div>

                  {application.suggested_improvements && (
                    <div className="mb-4 p-4 bg-yellow-50 rounded-md">
                      <p className="text-sm font-medium text-yellow-900 mb-2">Suggestions for Improvement:</p>
                      <ul className="list-disc list-inside text-sm text-yellow-800 space-y-1">
                        {JSON.parse(application.suggested_improvements).slice(0, 3).map((suggestion: any, idx: number) => (
                          <li key={idx}>{typeof suggestion === 'string' ? suggestion : suggestion.suggestion}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="flex flex-wrap gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDownloadResume(application.id, 'pdf')}
                    >
                      <Download className="h-4 w-4 mr-1" />
                      Download PDF
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDownloadResume(application.id, 'docx')}
                    >
                      <Download className="h-4 w-4 mr-1" />
                      Download DOCX
                    </Button>
                    {!application.cover_letter && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleGenerateCoverLetter(application.id)}
                      >
                        <Mail className="h-4 w-4 mr-1" />
                        Generate Cover Letter
                      </Button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Applications;


