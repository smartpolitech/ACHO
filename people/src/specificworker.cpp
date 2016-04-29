/*
 *    Copyright (C) 2016 by YOUR NAME HERE
 *
 *    This file is part of RoboComp
 *
 *    RoboComp is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    RoboComp is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "specificworker.h"

/**
* \brief Default constructor
*/
SpecificWorker::SpecificWorker(MapPrx& mprx) : GenericWorker(mprx)
{
   writeVideo("open");
}

/**
* \brief Default destructor
*/
SpecificWorker::~SpecificWorker()
{
}

bool SpecificWorker::setParams(RoboCompCommonBehavior::ParameterList params)
{
	timer.start(50);
	return true;
}

void SpecificWorker::compute()
{
  static QTime reloj = QTime::currentTime();
  try
  {
    //rgbd_proxy->getImage(image, depth, points, hState, bState);
    rgbd_proxy->getDepth(depth, hState, bState);
	   
    cv::Mat depthCV(240, 320, CV_32FC1,  &(depth)[0]), depth_norm, dd;
		
		std::vector< cv::Point2f> points;
		for(int i=0; i<depthCV.rows; i++)
			for(int j=0; j<depthCV.cols; j++) 
				if ( depthCV.at<float>(i,j) < 1400 and  depthCV.at<float>(i,j) > 1000)
				{
					points.push_back(cv::Point2f(i,j));
				}
				else
					depthCV.at<float>(i,j) = 0.f;

		cv::imshow("depthCV", depthCV);
		qDebug() << "points" << points.size();
		
		if( points.size() < 100)
		  return;
		
		int maxClusters = 3;
		cv::Mat indices, centers;
		cv::TermCriteria criteria(cv::TermCriteria::EPS + cv::TermCriteria::COUNT, 10, 1.0);
		
		double c = cv::kmeans(cv::Mat(points).reshape(1, points.size()), maxClusters, indices, criteria, maxClusters, cv::KMEANS_PP_CENTERS, centers );
		qDebug() << "Num centros" << centers.rows;
	
		std::vector<uint32_t> count;
		for (int i=0; i<maxClusters; i++)
			count.push_back(0);
	
		for (int i=0; i<indices.rows; i++)
			count[indices.at<int>(i)]++;
	
		cv::normalize( depthCV, depth_norm, 0, 255, cv::NORM_MINMAX, CV_32FC1, cv::Mat() );
		cv::convertScaleAbs( depth_norm, depth_norm );
		printf("%d %d\n", indices.rows, indices.cols);
	
		for (int row=0; row<centers.rows; row++)
		{
			printf("%d: %d\n", row, count[row]);
			if (count[row] > 200)
				cv::circle(depth_norm, cv::Point(centers.at<float>(row,1), centers.at<float>(row,0)), 40, cv::Scalar(255) );
		}
		cv::imshow("depth", depth_norm); 	
		  
  }
  catch(const Ice::Exception &e)
  {
    std::cout << "Error reading from Camera" << e << std::endl;
  }
}


void SpecificWorker::writeVideo(const QString &com, const cv::Mat& frame)
{
  static ofstream outputVideo;
  
  if( com == "open" )
  {
    outputVideo.open("pru.vid", ios::out | ios::binary);
    if (outputVideo.is_open() == false) {
      qFatal("Could not open the output video for write");
    }
    return;
  }
  if( com == "close")
  {
    outputVideo.close();
    return;
  }
  outputVideo.write(reinterpret_cast<const char*>(frame.data), frame.step[0] * frame.rows);
  
}

//cv::Mat SpecificWorker::readVideo(const QString &com)
//{
//   static ifstream video;
//   
//   if( com == "open" )
//   {
//     video.open("pru.vid", ios::in | ios::binary);
//     if (video.is_open() == false) {
//       qFatal("Could not open the output video for write");
//     }
//     return;
//   }
//   video.read(reinterpret_cast<const char*>(frame.data), frame.step[0] * frame.rows);
//   
//}




