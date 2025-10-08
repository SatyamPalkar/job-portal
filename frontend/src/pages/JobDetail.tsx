import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '@/components/Layout';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { jobApi, resumeApi, applicationApi } from '@/services/api';
import type { Job, Resume } from '@/types';
import { MapPin, Building2, Briefcase, ExternalLink, FileText } from 'lucide-react';

const JobDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null);
  const [optimizationLevel, setOptimizationLevel] = useState<'conservative' | 'balanced' | 'aggressive'>('balanced');
  const [isLoading, setIsLoading] = useState(true);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [showApplyForm, setShowApplyForm] = useState(false);

  useEffect(() => {
    if (id) {
      fetchJobAndResumes(parseInt(id));
    }
  }, [id]);

  const fetchJobAndResumes = async (jobId: number) => {
    setIsLoading(true);
    try {
      const [jobData, resumesData] = await Promise.all([
        jobApi.getById(jobId),
        resumeApi.getAll(),
      ]);
      setJob(jobData);
      setResumes(resumesData.filter(r => r.is_original));
      if (resumesData.length > 0) {
        setSelectedResumeId(resumesData[0].id);
      }
    } catch (error) {
      console.error('Error fetching job:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOptimizeAndApply = async () => {
    if (!job || !selectedResumeId) return;

    setIsOptimizing(true);
    try {
      // Optimize resume
      const optimizeResult = await resumeApi.optimize({
        resume_id: selectedResumeId,
        job_id: job.id,
        optimization_level: optimizationLevel,
      });

      alert(`Resume optimized successfully! Match score: ${optimizeResult.match_score}%`);
      
      // Navigate to applications page
      navigate('/applications');
    } catch (error) {
      console.error('Error optimizing resume:', error);
      alert('Failed to optimize resume. Please try again.');
    } finally {
      setIsOptimizing(false);
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-3/4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </Layout>
    );
  }

  if (!job) {
    return (
      <Layout>
        <Card>
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900">Job not found</h3>
            <Button onClick={() => navigate('/jobs')} className="mt-4">
              Back to Jobs
            </Button>
          </div>
        </Card>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h1>
            <div className="flex flex-wrap gap-4 text-gray-600">
              <div className="flex items-center">
                <Building2 className="h-5 w-5 mr-2" />
                {job.company}
              </div>
              {job.location && (
                <div className="flex items-center">
                  <MapPin className="h-5 w-5 mr-2" />
                  {job.location}
                </div>
              )}
              {job.job_type && (
                <div className="flex items-center">
                  <Briefcase className="h-5 w-5 mr-2" />
                  {job.job_type}
                </div>
              )}
            </div>
          </div>
          {job.source_url && (
            <a
              href={job.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center text-primary-600 hover:text-primary-700"
            >
              View on {job.source}
              <ExternalLink className="h-5 w-5 ml-2" />
            </a>
          )}
        </div>

        {job.salary_range && (
          <div className="inline-block px-4 py-2 bg-green-50 text-green-700 rounded-lg font-medium">
            {job.salary_range}
          </div>
        )}

        <Card title="Job Description">
          <div className="prose max-w-none">
            <p className="whitespace-pre-wrap text-gray-700">{job.description}</p>
          </div>
        </Card>

        {job.required_skills && (
          <Card title="Required Skills">
            <div className="flex flex-wrap gap-2">
              {JSON.parse(job.required_skills).map((skill: string, idx: number) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </Card>
        )}

        {/* Apply form */}
        <Card title="Apply with Optimized Resume">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Resume to Optimize
              </label>
              <select
                value={selectedResumeId || ''}
                onChange={(e) => setSelectedResumeId(parseInt(e.target.value))}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">Select a resume...</option>
                {resumes.map((resume) => (
                  <option key={resume.id} value={resume.id}>
                    {resume.title}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Optimization Level
              </label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'conservative', label: 'Conservative', desc: 'Minimal changes' },
                  { value: 'balanced', label: 'Balanced', desc: 'Recommended' },
                  { value: 'aggressive', label: 'Aggressive', desc: 'Maximum optimization' },
                ].map((level) => (
                  <button
                    key={level.value}
                    onClick={() => setOptimizationLevel(level.value as any)}
                    className={`p-4 border-2 rounded-lg text-left transition-colors ${
                      optimizationLevel === level.value
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="font-medium text-gray-900">{level.label}</div>
                    <div className="text-sm text-gray-500 mt-1">{level.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="flex space-x-3">
              <Button
                onClick={handleOptimizeAndApply}
                isLoading={isOptimizing}
                disabled={!selectedResumeId}
              >
                <FileText className="h-5 w-5 mr-2" />
                Optimize Resume & Apply
              </Button>
              <Button variant="outline" onClick={() => navigate('/jobs')}>
                Cancel
              </Button>
            </div>

            {resumes.length === 0 && (
              <p className="text-sm text-amber-600">
                You need to upload a resume first. <a href="/resumes" className="underline">Upload resume</a>
              </p>
            )}
          </div>
        </Card>
      </div>
    </Layout>
  );
};

export default JobDetail;


