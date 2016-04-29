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
	   
    cv::Mat depthCV(240, 320, CV_32FC1,  &(depth)[0]), depth_norm;
		//cv::threshold( depthCV, depthCV, 1300, 0, 4);
		//int npixels = cv::countNonZero(depthCV);
		//qDebug() << npixels;
		//if( npixels > 100)
		
			std::vector< cv::Point2f> points;
			int k=0;
			for(int i=0; i<depthCV.rows; i++)
				for(int j=0; j<depthCV.cols; j++) 
					if ( depthCV.at<float>(i,j) < 1300 )
					{
						points.push_back(cv::Point2f(i,j));
						k++;
					}
					else
						depthCV.at<float>(i,j) = 0.f;
		
			qDebug() << k << "points";
			if( k > 100)
			{
				cv::Mat indices, centers;
				cv::TermCriteria criteria(cv::TermCriteria::EPS + cv::TermCriteria::COUNT, 10, 1.0);
				double c = cv::kmeans(points, 3, indices, criteria, 3, cv::KMEANS_RANDOM_CENTERS, centers );
				//qDebug() << centers.at<float>(0,0) << centers.at<float>(0,1);
			}
			
		cv::normalize( depthCV, depth_norm, 0, 255, cv::NORM_MINMAX, CV_32FC1, cv::Mat() );
    cv::convertScaleAbs( depth_norm, depth_norm );  
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




