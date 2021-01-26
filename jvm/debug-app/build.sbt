lazy val root = (project in file("."))
  .settings(
    name := "debug-app",
    organization := "com.kiemlicz",
    description := "To debug things",
    licenses += "The MIT License" -> url("https://opensource.org/licenses/MIT"),
    scalacOptions ++= Seq(
      "-encoding", "utf8",
      "-deprecation",
      "-unchecked",
      "-Xlint",
    ),
    resolvers += "Sonatype releases".at("https://oss.sonatype.org/content/repositories/releases/"),
    libraryDependencies ++= Seq(),
    dockerBaseImage := "openjdk:11.0-jdk-slim"
  )
  .enablePlugins(JavaServerAppPackaging, DockerPlugin)