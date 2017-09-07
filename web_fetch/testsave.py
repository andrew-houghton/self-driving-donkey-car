 driver.get("http://www.google.com");
    WebElement image = driver.findElement(By.id("hplogo"));   
    //Get entire page screenshot
    File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
    BufferedImage  fullImg = ImageIO.read(screenshot);
    //Get the location of element on the page
    Point point = image.getLocation();
    //Get width and height of the element
    int imageWidth = image.getSize().getWidth();
    int imageHeight = image.getSize().getHeight();
    //Crop the entire page screenshot to get only element screenshot
    BufferedImage eleScreenshot= fullImg.getSubimage(point.getX(), point.getY(), imageWidth,
            imageHeight);
    ImageIO.write(eleScreenshot, "png", screenshot);
    //Copy the element screenshot to disk
    FileUtils.copyFile(screenshot, new File("E:\\selenium_desk\\GoogleLogo_screenshot1.png"));
    driver.close();