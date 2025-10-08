import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import Layout from '@/components/Layout';
import Card from '@/components/Card';
import Button from '@/components/Button';
import { resumeApi, jobApi, applicationApi } from '@/services/api';
import { FileText, Briefcase, ClipboardList, TrendingUp } from 'lucide-react';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    resumes: 0,
    jobs: 0,
    applications: 0,
    avgMatchScore: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [resumes, jobs, applications] = await Promise.all([
          resumeApi.getAll(),
          jobApi.getAll({ limit: 100 }),
          applicationApi.getAll(),
        ]);

        const avgScore = applications.length > 0
          ? applications.reduce((sum, app) => sum + (app.match_score || 0), 0) / applications.length
          : 0;

        setStats({
          resumes: resumes.length,
          jobs: jobs.length,
          applications: applications.length,
          avgMatchScore: Math.round(avgScore),
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  const statCards = [
    {
      title: 'Resumes',
      value: stats.resumes,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      link: '/resumes',
    },
    {
      title: 'Available Jobs',
      value: stats.jobs,
      icon: Briefcase,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      link: '/jobs',
    },
    {
      title: 'Applications',
      value: stats.applications,
      icon: ClipboardList,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      link: '/applications',
    },
    {
      title: 'Avg Match Score',
      value: `${stats.avgMatchScore}%`,
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      link: '/applications',
    },
  ];

  return (
    <Layout>
      <div className="space-y-8">
        {/* Welcome section */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.full_name || user?.username}!
          </h1>
          <p className="mt-2 text-lg text-gray-600">
            Here's your job application overview
          </p>
        </div>

        {/* Stats grid */}
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                <div className="h-12 bg-gray-200 rounded mb-4"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {statCards.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <Link key={index} to={stat.link}>
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                        <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                      </div>
                      <div className={`${stat.bgColor} p-3 rounded-lg`}>
                        <Icon className={`h-8 w-8 ${stat.color}`} />
                      </div>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        )}

        {/* Quick actions */}
        <Card title="Quick Actions" subtitle="Get started with common tasks">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link to="/resumes">
              <Button variant="outline" className="w-full">
                <FileText className="h-5 w-5 mr-2" />
                Upload Resume
              </Button>
            </Link>
            <Link to="/jobs">
              <Button variant="outline" className="w-full">
                <Briefcase className="h-5 w-5 mr-2" />
                Search Jobs
              </Button>
            </Link>
            <Link to="/applications">
              <Button variant="outline" className="w-full">
                <ClipboardList className="h-5 w-5 mr-2" />
                View Applications
              </Button>
            </Link>
          </div>
        </Card>

        {/* Getting started */}
        <Card title="Getting Started" subtitle="How to use Resume Optimizer">
          <div className="space-y-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary-100 text-primary-600 font-semibold">
                  1
                </div>
              </div>
              <div className="ml-4">
                <h4 className="text-lg font-medium text-gray-900">Upload Your Resume</h4>
                <p className="mt-1 text-gray-600">
                  Start by uploading your current resume in PDF, DOCX, or TXT format.
                </p>
              </div>
            </div>

            <div className="flex">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary-100 text-primary-600 font-semibold">
                  2
                </div>
              </div>
              <div className="ml-4">
                <h4 className="text-lg font-medium text-gray-900">Search for Jobs</h4>
                <p className="mt-1 text-gray-600">
                  Browse LinkedIn jobs or search for positions matching your skills.
                </p>
              </div>
            </div>

            <div className="flex">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary-100 text-primary-600 font-semibold">
                  3
                </div>
              </div>
              <div className="ml-4">
                <h4 className="text-lg font-medium text-gray-900">Optimize Your Resume</h4>
                <p className="mt-1 text-gray-600">
                  Let our AI optimize your resume for each specific job posting.
                </p>
              </div>
            </div>

            <div className="flex">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary-100 text-primary-600 font-semibold">
                  4
                </div>
              </div>
              <div className="ml-4">
                <h4 className="text-lg font-medium text-gray-900">Apply with Confidence</h4>
                <p className="mt-1 text-gray-600">
                  Download your optimized resume and apply to jobs with better match scores.
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </Layout>
  );
};

export default Dashboard;


