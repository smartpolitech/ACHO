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
	   
    cv::Mat depthCV(240, 320, CV_32FC1,  &(depth)[0]), depth_norm, depth_norm_scaled;
	
	cv::threshold( depthCV, depthCV, 1500, 0, 4);
	
    cv::normalize( depthCV, depth_norm, 0, 255, cv::NORM_MINMAX, CV_32FC1, cv::Mat() );
    cv::convertScaleAbs( depth_norm, depth_norm_scaled );  
    cv::imshow("depth", depth_norm_scaled);
    
	//double min, max;
	//cv::minMaxLoc(depthCV,&min,&max);
	
    //writeVideo("", depthCV);
    
//     if(reloj.elapsed() > 5000)
//     {
//       writeVideo("close");
//       qFatal("fary");
//     }
    
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




